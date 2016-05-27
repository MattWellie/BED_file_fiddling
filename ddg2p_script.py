
filename = "ddg2p.bed"
filename2 = "ddg2p_monoLoF_red_others_blue.bed"

first = True
pli_dict = {}
with open('pli_scores.txt', 'r') as handle:
    for line in handle:
        if first:
            first = False
        else:
            line_list = line.split('\t')
            gene = line_list[1].rstrip()
            pli = line_list[-1].rstrip()
            pli_dict[gene] = pli

with open(filename, 'r') as handle:
    with open(filename2, 'w') as outhandle:
        line = handle.readline()
        outhandle.write(line)
        while True:
            try:
                line = handle.readline()
                line_list = line.split('\t')
                colour = line_list[-1]
                details = line_list[3]
                detail_list = details.split('|')
                gene = detail_list[0]
                allelic = detail_list[1]
                mode = detail_list[2]
                # print '%s - %s - %s - %s' % (gene, allelic, mode, colour)
                if allelic == 'Monoallelic' and mode == 'Loss_of_function':
                    line_list[-1] = '255,0,0\n'
                else:
                    line_list[-1] = '0,0,255\n'
                if gene in pli_dict:
                    line_list[3] = '{}|pLI_score={}'.format(details, pli_dict[gene])
                outhandle.write('\t'.join(line_list))
            except:
                break