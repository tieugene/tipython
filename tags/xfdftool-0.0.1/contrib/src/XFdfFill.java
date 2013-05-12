package org.fillpdf;
import java.io.*;

import com.itextpdf.text.pdf.*;

public class XFdfFill {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		if (args.length != 3){
			 System.out.println("usage:");
			 System.out.println("xfdffill <out.pdf> <form.pdf> <data.xpdf>");
			 return;
		}

		try {
			PdfReader pdfreader = new PdfReader(args[1]);

			PdfStamper stamp = new PdfStamper(pdfreader, new FileOutputStream(args[0]));
			XfdfReader fdfreader = new XfdfReader(args[2]);
			AcroFields form = stamp.getAcroFields();
			form.setFields(fdfreader);
			stamp.close();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
}
