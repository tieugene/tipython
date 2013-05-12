/*
 * Stage1: show form fields
 */

package MyPkg;

import java.io.*;
import java.util.Set;

import com.itextpdf.text.pdf.*;

public class Stage1 {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		if (args.length != 1){
			 System.out.println("usage:");
			 System.out.println("Stage1 <file.pdf>");
			 return;
		}

		try {
			PdfReader	reader = new PdfReader(args[0]);
			AcroFields	form = reader.getAcroFields();
			XfaForm		xfaForm = form.getXfa();
			System.out.println(xfaForm.isXfaPresent());
			Set<String>	fields = form.getFields().keySet();
			for (String key : fields) {
			    System.out.print(key + ": ");
			    switch (form.getFieldType(key)) {
			    case AcroFields.FIELD_TYPE_CHECKBOX:
				System.out.println("Checkbox");
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
				System.out.println("Radiobutton");
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
			reader.close();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
}
