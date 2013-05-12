/*
 * Stage2: export xfdf/xdp
 */

package MyPkg;

import java.io.*;
import java.util.Set;

import com.itextpdf.text.pdf.*;

public class Stage2 {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		if (args.length != 1){
			 System.out.println("usage:");
			 System.out.println("Stage2 <file.pdf>");
			 return;
		}
		try {
			PdfReader	reader = new PdfReader(args[0]);
			FileOutputStream writer = new FileOutputStream("result.fdf");
			FdfWriter	fdfwriter = new FdfWriter();
			AcroFields	form = reader.getAcroFields();
			//fdfwriter.set
			form.exportAsFdf(fdfwriter);
			fdfwriter.writeTo(writer);
			writer.close();
			reader.close();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
}
