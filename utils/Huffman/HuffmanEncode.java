import java.io.IOException;

public class HuffmanEncode {
	public static void main(String[] args) throws IOException, ClassNotFoundException {

		if (args.length < 2) {
			System.out.println("Usage: java Huffman <input file> <output file>");
			return;
		}

		String inputFileName = args[0];
		String outputFileName = args[1];

		Huffman huffObj = new Huffman();

		huffObj.encode(inputFileName, outputFileName);		
	}
}
