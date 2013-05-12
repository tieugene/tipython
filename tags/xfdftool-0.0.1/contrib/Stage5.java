/*
 * Stage5: Populate field (XFA) - flatten
 */

package MyPkg;

import java.io.*;
import java.util.Set;

import com.itextpdf.text.pdf.*;

public class Stage5 {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		if (args.length != 2){
			 System.out.println("usage:");
			 System.out.println("Stage5 <template.pdf> <result.pdf>");
			 return;
		}
		try {
			PdfReader	reader = new PdfReader(args[0]);
			//PdfStamper	stamper = new PdfStamper(reader, new FileOutputStream(args[1]), '\0', true);
			PdfStamper	stamper = new PdfStamper(reader, new FileOutputStream(args[1]));
			stamper.setFormFlattening(true);
			// or:
			AcroFields	form = stamper.getAcroFields();
			form.setField("comb_1", "Петров");
			// or:
			//PdfDictionary root = reader.getCatalog();
			//PdfDictionary acroform = root.getAsDict(PdfName.ACROFORM);
			//acroform.remove(PdfName.XFA);
			//AcroFields	form = stamper.getAcroFields();
			//form.setField("topmostSubform[0].Page1[0].comb_1[0]", "Petroff");
			reader.close();
			stamper.close();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
}
