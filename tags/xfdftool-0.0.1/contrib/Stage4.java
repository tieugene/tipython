/*
 * Stage4: Populate field (AcroForm) - flatten
 */

package MyPkg;

import java.io.*;
import java.util.Set;

import com.itextpdf.text.pdf.*;

public class Stage4 {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		if (args.length != 2){
			 System.out.println("usage:");
			 System.out.println("Stage4 <template.pdf> <result.pdf>");
			 return;
		}
		try {
			PdfReader	reader = new PdfReader(args[0]);
			//PdfStamper	stamper = new PdfStamper(reader, new FileOutputStream(args[1]), '\0', true);
			PdfStamper	stamper = new PdfStamper(reader, new FileOutputStream(args[1]));
			stamper.setFormFlattening(true);
			AcroFields	form = stamper.getAcroFields();
			form.setField("title", "Ivanoff");
			reader.close();
			stamper.close();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
}
