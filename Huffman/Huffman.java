import java.io.*;
import java.util.ArrayList;
import net.datastructures.*;

public class Huffman {
	private class HuffmanTreeNode { 
	    private int character;
	    private int count;
	    private HuffmanTreeNode left;
	    private HuffmanTreeNode right;
	    public HuffmanTreeNode(int c, int ct, HuffmanTreeNode leftNode, HuffmanTreeNode rightNode) {
	    	character = c;
	    	count = ct;
	    	left = leftNode;
	    	right = rightNode;
	    }
	    public int getChar() { return character;}
	    public Integer getCount() { return count; }
	    public HuffmanTreeNode getLeft() { return left;}
	    public HuffmanTreeNode getRight() { return right;}
		public boolean isLeaf() { return left == null;}
	}
	
	private class OutBitStream {
		OutputStream out;
		int buffer;
		int buffCount;
		public OutBitStream(OutputStream output) {
			out = output;
			buffer=0;
			buffCount=0;
		}
		public void writeBit(int i) throws IOException {
		    buffer=buffer<<1;
		    buffer=buffer+i;
		    buffCount++;
		    if (buffCount==8) { 
		    	out.write(buffer); 
		    	buffCount=0;
		    	buffer=0;
		    }
		}
		public void close() throws IOException {
			if (buffCount>0) {
				buffer=buffer<<(8-buffCount);
				out.write(buffer);
			}
			out.close();
		}
 	}
	
	private class InBitStream {
		InputStream in;
		int buffer;
		int buffCount;
		public InBitStream(InputStream input) {
			in = input;
			buffer=0; 
			buffCount=8;
		}
		public int readBit() throws IOException {
			if (buffCount==8) {
				buffCount=0;
				buffer=in.read();
				if (buffer==-1) return -1;
			}
			int aux=128>>buffCount;
			buffCount++;
			if ((aux&buffer)>0) return 1;
			else return 0;
		}
	}
	
	private ArrayList<Integer> buildFrequencyTable(InputStream input) throws IOException{
		ArrayList<Integer> freqTable = new ArrayList<Integer>(257);
		for (int i=0; i<257;i++) freqTable.add(i,0);
		int buffer = input.read();
		while (buffer != -1) {
			freqTable.set(buffer, freqTable.get(buffer)+1);
			buffer = input.read();
		}
		freqTable.set(256, 1);
		return freqTable;
	}

	private HuffmanTreeNode buildEncodingTree(ArrayList<Integer> freqTable) {
		HeapPriorityQueue<Integer,HuffmanTreeNode> p = new HeapPriorityQueue<>();
		HuffmanTreeNode t;
		for (int i=0; i < freqTable.size(); i++) {
			if (freqTable.get(i) != 0) {
				t = new HuffmanTreeNode(i, freqTable.get(i), null, null);
				p.insert(t.count, t);
			}
		}
		Entry<Integer,HuffmanTreeNode> e1;
		Entry<Integer,HuffmanTreeNode> e2;
		while ( p.size() > 1 ) {
			e1 = p.removeMin();
			e2 = p.removeMin();
			t = new HuffmanTreeNode(0, 0, e1.getValue(), e2.getValue());
			p.insert(e1.getKey()+e2.getKey(), t);
		}
		e1 = p.removeMin();
		return e1.getValue();
	}
	
	private ArrayList<String> buildEncodingTable(HuffmanTreeNode encodingTreeRoot) {
		ArrayList<String> code= new ArrayList<String>(257); 
		for (int i=0;i<257;i++) code.add(i,null);
		ArrayStack<HuffmanTreeNode> nodes = new ArrayStack<>();
		HuffmanTreeNode current = encodingTreeRoot;
		ArrayStack<String> path = new ArrayStack<>();
		ArrayStack<String> tmp = new ArrayStack<>();
		HuffmanTreeNode p;
		StringBuffer string;
		while ( !nodes.isEmpty() || current != null ) {
			if ( current != null && current.isLeaf() ){
				string = new StringBuffer();
				while ( !path.isEmpty() ) {
					string.append( path.top() );
					tmp.push( path.pop() );
				}
				code.set(current.character, string.reverse().toString());
				while ( !tmp.isEmpty() ) {
					path.push( tmp.pop() );
				}
			}
			if (current != null) {
				nodes.push(current);
				current = current.left;
				if (current != null)
					path.push("0");
			}
			else {
				HuffmanTreeNode node = nodes.pop();
				if ( node != null && node.left != null){
					p = node.left;
					while(p.right != null){
						path.pop();
						p = p.right;
					}
				}
				path.pop();
				current = node.right;
				path.push("1");
			}
		}
		return code;
	}
	
	private void encodeData(InputStream input, ArrayList<String> encodingTable, OutputStream output) throws IOException {
		OutBitStream bitStream = new OutBitStream(output);
		int buffer = input.read();
		while (buffer != -1) {
			for (int i=0; i < encodingTable.get(buffer).split("").length; i++) {
				bitStream.writeBit( Integer.parseInt(encodingTable.get(buffer).split("")[i]) );
			}
			buffer = input.read();
		}
		for (int i=0; i < encodingTable.get(256).split("").length; i++) {
				bitStream.writeBit( Integer.parseInt(encodingTable.get(256).split("")[i]) );	
		}
		bitStream.close();
	}
	
	private void decodeData(ObjectInputStream input, HuffmanTreeNode encodingTreeRoot, FileOutputStream output) throws IOException {
		InBitStream inputBitStream = new InBitStream(input);
		HuffmanTreeNode p;
		int buffer = inputBitStream.readBit();
		while (buffer != -1) {
			p = encodingTreeRoot;
			while (buffer != -1 && !p.isLeaf() ){
				if (buffer == 0) 
					p = p.left;
				else
					p = p.right;

				buffer = inputBitStream.readBit();
			}
			if (p.character == 256)
				return;
			output.write(p.character);
		}
    }
	
	public void encode(String inputFileName, String outputFileName) throws IOException {
		System.out.println("\nEncoding "+inputFileName+ " " + outputFileName);
		FileInputStream input = new FileInputStream(inputFileName);
		FileInputStream copyinput = new FileInputStream(inputFileName);
		FileOutputStream out = new FileOutputStream(outputFileName);
 		ObjectOutputStream codedOutput = new ObjectOutputStream(out);
		ArrayList<Integer> freqTable = buildFrequencyTable(input);
		HuffmanTreeNode root = buildEncodingTree(freqTable);
		ArrayList<String> codes = buildEncodingTable(root);
		codedOutput.writeObject(freqTable);
		encodeData(copyinput, codes, codedOutput);
	}
	
	public void decode (String inputFileName, String outputFileName) throws IOException, ClassNotFoundException {
		System.out.println("\nDecoding "+inputFileName+ " " + outputFileName);
		FileInputStream in = new FileInputStream(inputFileName);
 		ObjectInputStream codedInput = new ObjectInputStream(in);
 		FileOutputStream output = new FileOutputStream(outputFileName);
		ArrayList<Integer> freqTable = (ArrayList<Integer>) codedInput.readObject();
		HuffmanTreeNode root = buildEncodingTree(freqTable);
		decodeData(codedInput, root, output);
	}
}
 