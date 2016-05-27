"""
Script to re-process A BED file (specifically the DDG2P BED file) to change colors and add annotations
"""

filename = "ddg2p.bed"
filename2 = "ddg2p_monoLoF_red_others_blue.bed"

"""
Go through a text file containing pLI scores, skip the first row
For every other row, find the gene name and pLI scores, add to a dictionary, indexed by Gene
"""
first = True
pli_dict = {}
with open('pli_scores.txt', 'r') as handle:
    for line in handle:
        # Skip line 1
        if first:
            first = False
        else:
            # Split the whole row by tabs
            line_list = line.split('\t')
            # Use rstript to remove all whitespace for an accurate text match
            gene = line_list[1].rstrip()
            pli = line_list[-1].rstrip()
            pli_dict[gene] = pli

# open the DDG2P BED file
with open(filename, 'r') as handle:
    with open(filename2, 'w') as outhandle:
        # Before looping, copy the first line straight over
        line = handle.readline()
        outhandle.write(line)
        while True:
            try:
                # Get the specified elements from the line
                line = handle.readline()
                line_list = line.split('\t')
                colour = line_list[-1]
                # 'Details' contains multiple sections
                details = line_list[3]
                detail_list = details.split('|')
                gene = detail_list[0]
                allelic = detail_list[1]
                mode = detail_list[2]
                # print '%s - %s - %s - %s' % (gene, allelic, mode, colour)
                # This was the chosen priority for colours
                # Mono-LoF red, everything else Blue
                if allelic == 'Monoallelic' and mode == 'Loss_of_function':
                    line_list[-1] = '255,0,0\n'
                else:
                    line_list[-1] = '0,0,255\n'
                # Check the indices of the pli dict, if the gene is present, add pLI score
                if gene in pli_dict:
                    line_list[3] = '{}|pLI_score={}'.format(details, pli_dict[gene])
                outhandle.write('\t'.join(line_list))
            except:
                break
