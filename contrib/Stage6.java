/*
 * Stage6: Populate fields w/ XFDF (AcroForm)
 */

package MyPkg;

import java.io.*;
import java.util.Set;

import com.itextpdf.text.pdf.*;

public class Stage6 {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		if (args.length != 3) {
			 System.out.println("usage:");
			 System.out.println("Stage6 <template.pdf> <data.xfdf> <result.pdf>");
			 return;
		}
		try {
			PdfReader	reader = new PdfReader(args[0]);
			//PdfStamper	stamper = new PdfStamper(reader, new FileOutputStream(args[2]));
			PdfStamper	stamper = new PdfStamper(reader, System.out);
			stamper.setFormFlattening(true);
			XfdfReader	fdfreader = new XfdfReader(args[1]);
			AcroFields	form = stamper.getAcroFields();
			form.setFields(fdfreader);
			stamper.close();
			reader.close();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
}
