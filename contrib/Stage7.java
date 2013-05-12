/*
 * Stage6: Populate fields w/ XFDF (AcroForm)
 */

package MyPkg;

import java.io.*;
import java.util.Set;

import com.itextpdf.text.pdf.*;

public class Stage7 {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		if (args.length != 1) {
			System.out.println("Usage:\nStage7 <template.pdf> < data.xfdf > result.pdf");
			return;
		}
		try {
			PdfReader	reader = new PdfReader(args[0]);
			//PdfStamper	stamper = new PdfStamper(reader, new FileOutputStream(args[2]));
			PdfStamper	stamper = new PdfStamper(reader, System.out);
			stamper.setFormFlattening(true);
			//XfdfReader	fdfreader = new XfdfReader(args[1]);
			XfdfReader	fdfreader = new XfdfReader(System.in);
			AcroFields	form = stamper.getAcroFields();
			form.setFields(fdfreader);
			stamper.close();
			reader.close();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
}
