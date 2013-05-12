/*
 * apache-commons-cli, itext
 * Modes:
 * - info + fieldlist (w/o option)
 * - generate xfdf (> stdout)
 * - fill form <stdin >stdout
 */

package MyPkg;

import java.io.*;
import java.util.Set;

import com.itextpdf.text.pdf.*;	// 5.x

public class xfdftool {
	/**
	 * @param args
	 */
	private static String PrintValues(AcroFields form, String key) {
		String states[] = form.getAppearanceStates(key);
		String retvalue = "";
		String separator = "";
		for (int i = 0; i < states.length; i++) {
			retvalue = retvalue + separator + states[i];
			separator = ", ";
		}
		return retvalue;
	}
	private static void Info(PdfReader reader) {
		AcroFields	form = reader.getAcroFields();
		System.out.println("PDF Version: 1." + reader.getPdfVersion());
		System.out.println("XFA: " + form.getXfa().isXfaPresent());
		System.out.println("Fields:");
		Set<String>	fields = form.getFields().keySet();
		for (String key : fields) {
			System.out.print(key + ": ");
			switch (form.getFieldType(key)) {
				case AcroFields.FIELD_TYPE_CHECKBOX:
					System.out.println("Checkbox (" + PrintValues(form , key) + ")");
				break;
				case AcroFields.FIELD_TYPE_COMBO:
					System.out.println("Combobox");
					break;
				case AcroFields.FIELD_TYPE_LIST:
					System.out.println("List");
					break;
				case AcroFields.FIELD_TYPE_NONE:
					System.out.println("None");
					break;
				case AcroFields.FIELD_TYPE_PUSHBUTTON:
					System.out.println("Pushbutton");
					break;
				case AcroFields.FIELD_TYPE_RADIOBUTTON:
					System.out.println("Radiobutton (" + PrintValues(form , key) + ")");
					break;
				case AcroFields.FIELD_TYPE_SIGNATURE:
					System.out.println("Signature");
					break;
				case AcroFields.FIELD_TYPE_TEXT:
					System.out.println("Text");
					break;
				default:
					System.out.println("?");
			}
		}
	}
	private static void XfdfExport(PdfReader reader) {
		AcroFields	form = reader.getAcroFields();
		System.out.println("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<xfdf xmlns=\"http://ns.adobe.com/xfdf/\" xml:space=\"preserve\">\n <fields>");
		Set<String>	fields = form.getFields().keySet();
		for (String key : fields) {
			System.out.println("  <field name=\"" + key + "\">\n   <value>  </value>\n  </field>");
		}
		System.out.println(" </fields>\n</xfdf>");
	}
	//public static void PopulateForm(PdfReader reader) {}
	public static void main(String[] args) {
		String usage = "Usage:\n" +
			"\txfdftool <mode> <template.pdf> [< data.xfdf] [> result.txt|xfdf|pdf]\n" +
			"Mode:\n" +
			"\t-i/I - info (version, XFA comatibility, field names)\n" +
			"\t-e/E - export XFDF template\n" +
			"\t-f/F - populate PDF with XFDF\n" +
			"Note: I/E/F  - short names for XFA";
		if (args.length != 2) {
			System.err.println("Wrong parms qty: " + args.length);
			System.err.println(usage);
			return;
		}
		try {
			// 1. parse opts
			int mode = 0;
			String cmode = args[0];
			String smode = cmode.toLowerCase();
			if (smode.equals("-i")) {
				mode = 1;
			} else if (smode.equals("-e")) {
				mode = 2;
			} else if (smode.equals("-f")) {
				mode = 3;
			} else {
				System.err.println(usage);
				return;
			}
			boolean submode = smode.equals(cmode);	// True if lowcase
			// 2. create objects: mode, submode, form, input, output
			PdfReader	reader = new PdfReader(args[1]);
			// 3. do it
			switch (mode) {
				case (1):
					Info(reader);
					break;
				case (2):
					XfdfExport(reader);
					break;
				case (3):
					//PopulateForm(reader);
					PdfStamper stamper = new PdfStamper(reader, System.out);
					stamper.setFormFlattening(true);
					stamper.getAcroFields().setFields(new XfdfReader(System.in));
					stamper.close();
					break;
				default:
					break;
			}
			// 4. close all
			reader.close();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
}
