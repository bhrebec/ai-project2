import java.io.*;
/** This program verifies the correctness of form of an entry to the 2011 Pummill Relays computer 
* programming problem, held at Missouri State University Apr. 20, 2011. The expected form of each
* of the entered files is a file in plain text format, containing on separate lines integers 
* representing the following information: 
*		the number of lines in the file (including this line)
*		an ID number of a vertex in the set
*		an ID number of a vertex in the set
*		an ID number of a vertex in the set
* 			. 
*			  .
*			  	.
*
*
* This program expects as a parameter the filename to be checked.
*/
class FileTest {

	public static void main(String[] args) {
		FileTest ft = new FileTest();
		
		try {
			ft.readFile(args[0]);
		} catch(ArrayIndexOutOfBoundsException e) {  // Missing the required filename parameter!
			System.out.println("\n\tError: Must use as parameter the filename to be checked.\n");
			System.exit(0);
		}

	}

	void readFile(String file) {
		int num_lines = 0;			//number of supposed lines
		int act_lines = 0;			//number of actual lines
		int current_data = 0; 		// data on current line of file
		
		try {
			FileReader f = new FileReader(file);
			BufferedReader br = new BufferedReader(f);
			
			String s;
			
			if((s = br.readLine()) != null) {			//read in number of lines including this line
				num_lines = Integer.parseInt(s);		//turn into integer
				act_lines++;							//increase actual lines
				while((s = br.readLine()) != null) {
					current_data = Integer.parseInt(s);	//turn into integer
					act_lines++;						//read each line
					
					if (current_data < 0) {	// Check data begins at 0
						System.out.println("\n\tError: Data at file line " + (act_lines) + " is negative.");
						System.exit(0);
					}

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
			System.out.println("\n\tError: Data at file line " + (act_lines+1) + " is empty or non-integer.");
			System.exit(0);
		}
		
		if(num_lines == act_lines) {
			System.out.println("\n\tThe file is in the correct format.\nSupposed lines: " + num_lines + "\nActual Lines: " + act_lines);
		} else {
			System.out.println("\n\tError: The file is not in the correct format." +
				"\n\tSupposed lines: " + num_lines + 
				"\n\tActual Lines: " + act_lines);
		}
	}


}