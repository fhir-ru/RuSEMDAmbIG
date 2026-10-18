import java.nio.file.*;
import java.io.*;
import java.util.*;
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
    check(engine,"explicit_unit_no_consumer_text_allowed",explicitUnit,dosage,true);
    Map<String,Object> report=new LinkedHashMap<>();report.put("engine","org.hl7.fhir.r5.fhirpath.FHIRPathEngine from input-cache/publisher.jar");report.put("method","evaluateToBoolean");report.put("expressions_source","generated StructureDefinition differential constraints");report.put("passed",true);report.put("checks",RESULTS);
    Files.writeString(Path.of("reports/profile-rule-checks.json"),new GsonBuilder().setPrettyPrinting().disableHtmlEscaping().create().toJson(report)+"\n");
    System.out.println("6 profile FHIRPath runtime controls PASS");
  }
}
