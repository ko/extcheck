def write_to_csv(outfile, list):
    if not list:
        return 0
    with open(outfile, 'wb') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerows(list)
    return len(list)
 
