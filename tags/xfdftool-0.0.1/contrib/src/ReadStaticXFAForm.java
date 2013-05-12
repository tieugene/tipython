package MyPkg;

import java.io.IOException;
import com.lowagie.text.pdf.AcroFields;
import com.lowagie.text.pdf.PdfReader;
import com.lowagie.text.pdf.XfaForm;
import com.lowagie.text.pdf.XfaForm.Xml2SomDatasets;

public class ReadStaticXFAForm {

	public static final String RESULTING_INSTANCE = "resources/Acro8 Static XFA Instance.pdf";
	
	public static void main(String[] args) {
		try {

			PdfReader reader = new PdfReader(RESULTING_INSTANCE);
			AcroFields	form = reader.getAcroFields();

//		   XfaForm xfaForm = form.getXfa();
//			System.out.println(xfaForm.isXfaPresent());
//			Xml2SomDatasets xml2s = xfaForm.getDatasetsSom();

			System.out.println(form.getField("MyTextField"));
			reader.close();						
		} catch (IOException e) {
			e.printStackTrace();
		} 
	}
}