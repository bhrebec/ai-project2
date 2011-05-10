import java.io.*;
/** This program reads 2011 Pummill problem data from a CSV file. That file is expected
* to be a CSV file of rows of the form
*    name,1,1,0,1,1...
*    name,1,1,1,0,1...
*      . . . .
* where the 1's and 0's are an adjacency matrix of a graph. The CSC file contains a 
* square matrix which is already properly reflected about the diagonal.
*
* This program expects two parameters: 
*     
*     the number of lines in the CSV file
*     the CSV filename from which to read
*/
class ReadData2011 {

	public String names[];
	public char friends[][];
	
	public static void main(String[] args) {
		ReadData2011 ft = new ReadData2011();
		
		try {
			ft.readFile(Integer.parseInt(args[0]), args[1]);
		} catch(ArrayIndexOutOfBoundsException e) {  // Missing the required filename parameter!
			System.out.println("\n\tError: Run this program with two parameters:   numRows  filename \n");
			System.exit(0);
		}

	}

	void readFile(int size, String file) {
		int num_lines = 0;			//number of supposed lines
		int act_lines = 0;			//number of actual lines
		int current_data = 0; 		// data on current line of file
		int startIntStringIndex;
		int endIntStringIndex;
		
		// size = 10;  // Debug only
		
		names = new String[size];
		friends = new char[size][size];
		
		short dataArray[][] = new short[size][size];  // copy of the matrix
		short data;
		String s = null, t;
		
		try {
			FileReader f = new FileReader(file);
			BufferedReader br = new BufferedReader(f);
			

			
			if((s = br.readLine()) != null) {			//read in entire line (it's in the form      name,1,1,1,1,1...

				//System.out.println("String read is    ***" + s + "***");
			
				startIntStringIndex = 0;  // set the initial index 
				
				for (int row = 0; row < size; row++)
				{

					endIntStringIndex = s.indexOf(',', startIntStringIndex + 1);  // find the index of the separating comma
				
					names[row] = s.substring(startIntStringIndex, endIntStringIndex);  // read the name from that position
					startIntStringIndex = endIntStringIndex + 1;    


					for (int col = 0; col < size; col++)
					{
						endIntStringIndex = s.indexOf(',', startIntStringIndex + 1);  // find the index of the separating comma

						//System.out.println("Reading string from " + startIntStringIndex + " to " + endIntStringIndex);

						if (endIntStringIndex > 0)  // if there is a comma on this line, read the int prior to that comma
						{
							t = s.substring(startIntStringIndex, endIntStringIndex);  // read the int from that position
							//num_lines = Integer.parseInt(s);		//turn into integer
						}
						else
						{
							t = s.substring(startIntStringIndex, s.length() ); // ... otherwise, there are no more commas and t represents the last int on the line
						}
					
						startIntStringIndex = endIntStringIndex + 1;  

						// System.out.println(i + "  Data read is    ***" + t + "*** = "  + Integer.parseInt(t));
						
						data = (short)Integer.parseInt(t);  
						
						friends[row][col] = (char)data;
						
							
					
					}
					
					s = br.readLine();  // get next line
			
				} // end for

				
				// Show the friendships in the graph
				for (int row = 0; row < 10; row++)
				{
					
					for (int col = 0; col < 10; col++)
					{
						
						if ( (int)(friends[row][col]) > 0)
							System.out.println( names[row] + " is friends with " + names[col]);
							
					}
					System.out.println();
				}

				
			} else {
				System.out.println("\n\tError: The file is empty.");
				System.exit(0);
			}
		} 
		catch(IOException e) {
			e.printStackTrace();
		}
		catch(NumberFormatException e) {
			System.out.println("\n\tError: Data at file line " + (act_lines+1) + " is empty or non-integer.\n" + s);
			System.exit(0);
		}
		
		
	}


}