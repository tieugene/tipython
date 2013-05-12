package MyPkg;

import java.io.FileOutputStream;
import java.io.IOException;
import com.lowagie.text.DocumentException;
import com.lowagie.text.pdf.AcroFields;
import com.lowagie.text.pdf.PdfReader;
import com.lowagie.text.pdf.PdfStamper;


public class FillStaticXFAForm {

	public static final String FORM_TEMPLATE = "resources/Acro8 Static XFA Form.pdf";
	public static final String RESULTING_INSTANCE = "resources/Acro8 Static XFA Instance.pdf";
	
	public static void main(String[] args) {
		try {

			PdfReader reader = new PdfReader(FORM_TEMPLATE);
			PdfStamper stamper = new PdfStamper(reader, new FileOutputStream(RESULTING_INSTANCE), '\0', true);
			AcroFields	form = stamper.getAcroFields();
			form.setField("MyTextField", "sample text");
			reader.close();
			stamper.close();
						
		} catch (IOException e) {
			e.printStackTrace();
		} catch (DocumentException e) {
			e.printStackTrace();
		}
	}
}