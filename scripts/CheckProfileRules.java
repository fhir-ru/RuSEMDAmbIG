import java.nio.file.*;
import java.io.*;
import java.util.*;
import java.lang.reflect.Proxy;
import org.hl7.fhir.r5.fhirpath.IHostApplicationServices;
import com.google.gson.*;
import org.hl7.fhir.r5.fhirpath.FHIRPathEngine;
import org.hl7.fhir.r5.context.SimpleWorkerContext;
import org.hl7.fhir.r5.formats.JsonParser;
import org.hl7.fhir.r5.model.*;
import org.hl7.fhir.utilities.npm.NpmPackage;

/** Executes generated profile expressions with Publisher's actual R5 FHIRPath runtime. */
public class CheckProfileRules {
  static final JsonParser PARSER = new JsonParser();
  static final List<Map<String,Object>> RESULTS = new ArrayList<>();
  static Resource read(String path) throws Exception { try (var input = Files.newInputStream(Path.of(path))) { return PARSER.parse(input); } }
  static String expression(String profile, String key) throws Exception {
    StructureDefinition sd = (StructureDefinition)read("fsh-generated/resources/StructureDefinition-"+profile+".json");
    for (var element : sd.getDifferential().getElement())
      for (var rule : element.getConstraint()) if (rule.getKey().equals(key)) return rule.getExpression();
    throw new IllegalStateException("Generated constraint not found: "+key);
  }
  static void check(FHIRPathEngine engine, String name, Resource resource, String expression, boolean expected) {
    boolean actual = engine.evaluateToBoolean(resource, resource, resource, expression);
    RESULTS.add(Map.of("name",name,"expression",expression,"expected",expected,"actual",actual,"passed",actual==expected));
    if(actual!=expected) throw new IllegalStateException("Unexpected result "+name+": "+actual);
  }
  public static void main(String[] args) throws Exception {
    if (args.length!=1) throw new IllegalArgumentException("Pass local hl7.fhir.r5.core#5.0.0 package directory");
    var context = new SimpleWorkerContext.SimpleWorkerContextBuilder().withAllowLoadingDuplicates(true).fromPackage(NpmPackage.fromFolder(args[0]));
    var engine = new FHIRPathEngine(context);
    String first = expression("semd-amb-bundle","amb-composition-first");
    String dosage = expression("semd-amb-medication-statement","amb-smnn-dose-text");
    Bundle bundle = (Bundle) read("input/examples/Bundle-semd-amb-consultation-example.json");
    MedicationStatement statement = null;
    for(var entry:bundle.getEntry()) if(entry.getResource() instanceof MedicationStatement) statement=(MedicationStatement)entry.getResource();
    if(statement==null) throw new IllegalStateException("No MedicationStatement example");
    check(engine,"bundle_positive",bundle,first,true);
    Bundle wrongFirst=bundle.copy(); Collections.swap(wrongFirst.getEntry(),0,1);
    check(engine,"bundle_noncomposition_first_negative",wrongFirst,first,false);
    check(engine,"smnn_dose_text_positive",statement,dosage,true);
    MedicationStatement noText=statement.copy(); for(var dose:noText.getDosage())dose.setText(null);
    check(engine,"smnn_dose_text_removed_negative",noText,dosage,false);
    MedicationStatement otherSystem=noText.copy(); otherSystem.getMedication().getConcept().getCodingFirstRep().setSystem("https://example.org/non-smnn");
    check(engine,"non_smnn_no_text_allowed",otherSystem,dosage,true);
    MedicationStatement explicitUnit=noText.copy();
    explicitUnit.getDosageFirstRep().getDoseAndRateFirstRep().getDoseQuantity().setUnit("таблетка");
    check(engine,"dose_text_rule_alone_does_not_check_unit_legality",explicitUnit,dosage,true);
    String period=expression("semd-amb-medication-statement","amb-period-pair");
    check(engine,"therapy_period_pair_positive",statement,period,true);
    MedicationStatement oneBoundary=statement.copy(); oneBoundary.getEffectivePeriod().setEnd(null);
    check(engine,"therapy_missing_period_end_negative",oneBoundary,period,false);
    String duration=expression("semd-amb-medication-statement","amb-therapy-period-or-duration");
    check(engine,"therapy_period_without_duration_positive",statement,duration,true);
    MedicationStatement byDuration=statement.copy(); byDuration.setEffective(null);
    byDuration.addExtension("https://fhir.ru/ig/semd/amb/StructureDefinition/semd-amb-therapy-duration",new Duration().setValue(7).setCode("d"));
    check(engine,"therapy_duration_without_start_date_positive",byDuration,duration,true);
    MedicationStatement both=statement.copy(); both.getExtension().addAll(byDuration.getExtension());
    check(engine,"therapy_period_and_duration_negative",both,duration,false);
    check(engine,"smnn_unit_absent_positive",statement,expression("semd-amb-medication-statement","amb-smnn-dose-unit"),true);
    check(engine,"smnn_unit_present_negative",explicitUnit,expression("semd-amb-medication-statement","amb-smnn-dose-unit"),false);
    check(engine,"non_smnn_missing_unit_negative",otherSystem,expression("semd-amb-medication-statement","amb-smnn-dose-unit"),false);
    Observation visit=new Observation().setStatus(Enumerations.ObservationStatus.UNKNOWN);
    visit.setCode(new CodeableConcept().addCoding(new Coding("urn:oid:1.2.643.5.1.13.13.99.2.166","800",null)));
    visit.setValue(new CodeableConcept().addCoding(new Coding("urn:oid:1.2.643.5.1.13.13.11.1007","2",null)));
    check(engine,"mandatory_visit_value_positive",visit,expression("semd-amb-entry-1","amb-entry-1-value"),true);
    visit.setValue(null);
    check(engine,"mandatory_visit_value_removed_negative",visit,expression("semd-amb-entry-1","amb-entry-1-value"),false);
    visit.setDataAbsentReason(new CodeableConcept().setText("unknown"));
    check(engine,"R_value_cannot_be_replaced_by_absence",visit,expression("semd-amb-entry-1","amb-entry-1-value"),false);
    check(engine,"non_R_value_can_have_absence",visit,expression("semd-amb-entry-6","amb-entry-6-value"),true);
    Observation other=new Observation().setCode(new CodeableConcept());
    other.getCode().addExtension("http://hl7.org/fhir/StructureDefinition/iso21090-nullFlavor",new CodeType("OTH"));
    check(engine,"OTH_without_text_negative",other,expression("semd-amb-observation","amb-oth-code-text"),false);
    other.getCode().setText("Некодируемое понятие");
    check(engine,"OTH_with_text_positive",other,expression("semd-amb-observation","amb-oth-code-text"),true);
    Observation score=new Observation();
    check(engine,"empty_score_negative",score,expression("semd-amb-entry-37","amb-score-content"),false);
    score.setValue(new Quantity().setValue(5));
    check(engine,"score_result_positive",score,expression("semd-amb-entry-37","amb-score-content"),true);
    Composition composition=(Composition)bundle.getEntryFirstRep().getResource();
    String contextRule=expression("semd-amb-composition","amb-document-context");
    check(engine,"document_context_positive",composition,contextRule,true);
    Composition missingRecipient=composition.copy();
    for(var section:missingRecipient.getSection()) for(var subsection:section.getSection())
      subsection.getExtension().removeIf(e -> e.getUrl().endsWith("semd-amb-context-role") && e.getValue().primitiveValue().equals("recipient"));
    check(engine,"document_recipient_role_removed_negative",missingRecipient,contextRule,false);
    Map<String,Resource> targets=new HashMap<>();
    for(var e:bundle.getEntry())targets.put(e.getFullUrl(),e.getResource());
    engine.setHostServices((IHostApplicationServices)Proxy.newProxyInstance(
      IHostApplicationServices.class.getClassLoader(),new Class<?>[]{IHostApplicationServices.class},
      (proxy,method,arguments)->{
        if(method.getName().equals("resolveReference"))return targets.get((String)arguments[2]);
        if(method.getName().equals("findContainingResource"))return bundle;
        if(method.getName().equals("log"))return false;
        throw new UnsupportedOperationException("Unexpected FHIRPath host call: "+method.getName());
      }));
    String closure=expression("semd-amb-bundle","amb-document-references");
    check(engine,"document_references_resolved_positive",bundle,closure,true);
    Bundle missingTarget=bundle.copy();
    ((Composition)missingTarget.getEntryFirstRep().getResource()).getSectionFirstRep().getEntryFirstRep().setReference("urn:uuid:missing-resource");
    check(engine,"document_unresolved_clinical_reference_negative",missingTarget,closure,false);
    String sections=expression("semd-amb-composition","amb-section-docinfo-entries");
    boolean docinfoOK=engine.evaluateToBoolean(composition,composition,composition.getSectionFirstRep(),sections);
    if(!docinfoOK)throw new IllegalStateException("DOCINFO does not satisfy source cardinalities");
    Composition missingVisit=composition.copy();
    missingVisit.getSectionFirstRep().getEntry().remove(0);
    boolean missingVisitOK=engine.evaluateToBoolean(missingVisit,missingVisit,missingVisit.getSectionFirstRep(),sections);
    RESULTS.add(Map.of("name","docinfo_required_visit_resolved_positive_negative","positive",docinfoOK,"negative",missingVisitOK,"passed",docinfoOK&&!missingVisitOK));
    if(missingVisitOK)throw new IllegalStateException("Missing required visit was accepted");
    Observation disability=(Observation)targets.values().stream().filter(r -> r instanceof Observation && ((Observation)r).getCode().getCoding().stream().anyMatch(c -> c.getCode().equals("4058"))).findFirst().orElseThrow();
    String detail=expression("semd-amb-entry-13","amb-entry-13-details");
    check(engine,"required_disability_detail_positive",disability,detail,true);
    Observation missingDetail=disability.copy(); missingDetail.getHasMember().clear();
    check(engine,"required_disability_detail_removed_negative",missingDetail,detail,false);
    int sectionsVerified=0;
    for(var section:composition.getSection()) {
      if(!section.hasCode())continue;
      String sectionCode=section.getCode().getCodingFirstRep().getCode();
      if(sectionCode.equals("IMM"))continue;
      String sectionRule=expression("semd-amb-composition","amb-section-"+sectionCode.toLowerCase()+"-entries");
      if(!engine.evaluateToBoolean(composition,composition,section,sectionRule))throw new IllegalStateException("Source cardinality rule failed in "+sectionCode);
      sectionsVerified++;
    }
    RESULTS.add(Map.of("name","all_present_section_cardinalities","sections",sectionsVerified,"passed",true));
    Map<String,Object> report=new LinkedHashMap<>();report.put("engine","org.hl7.fhir.r5.fhirpath.FHIRPathEngine from input-cache/publisher.jar");report.put("method","evaluateToBoolean");report.put("expressions_source","generated StructureDefinition differential constraints");report.put("passed",true);report.put("checks",RESULTS);
    Files.writeString(Path.of("reports/profile-rule-checks.json"),new GsonBuilder().setPrettyPrinting().disableHtmlEscaping().create().toJson(report)+"\n");
    System.out.println(RESULTS.size()+" profile FHIRPath runtime controls PASS");
  }
}
