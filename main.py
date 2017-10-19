import concatenation
import mapping

def main():
    #concatenation
    concatProc = concatenation.Concatenation("concatInput.txt")
    concatProc.run_concat()
    #mapping
    mappingProc = mapping.Mapping("mappingInput.txt")
    mappingProc.run_mapping()



if __name__ == "__main__":
    main()
