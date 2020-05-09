import concatenation
import mapping

def main():
    #concatenation
    concat = raw_input("Are you going to run concatenation? (y/n)")
    ran_concatenation = (concat == 'y')
    if(ran_concatenation):
    	concatProc = concatenation.Concatenation("concatInput.txt")
    	concatProc.run_concat()
    #mapping
    mappingProc = mapping.Mapping("mappingInput.txt", ran_concatenation)
    mappingProc.run_mapping()



if __name__ == "__main__":
    main()
