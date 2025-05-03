import argparse
import sys
import os

def main():
    parser = argparse.ArgumentParser(
        description="XIWA Air Crackers - Web Information Gathering & Password Cracking Tool",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument('-v', '--viewer',
                        help='View website source code, server IP and developer email',
                        metavar='URL')
    
    parser.add_argument('-c', '--code',
                        help='Save website source code to output directory',
                        action='store_true')
    
    parser.add_argument('-s', '--sniff',
                        help='Enable network sniffing mode',
                        action='store_true')
    
    parser.add_argument('-f', '--file',
                        help='Output file for sniffed data')
    
    parser.add_argument('-crack', '--cracker',
                        choices=['instagram', 'github'],
                        help='Password cracking mode for specified platform')
    
    parser.add_argument('-u', '--username',
                        help='Username for password cracking')
    
    parser.add_argument('-m', '--min',
                        type=int,
                        help='Minimum password length',
                        default=8)
    
    parser.add_argument('-max', '--max',
                        type=int,
                        help='Maximum password length',
                        default=16)

    parser.add_argument('-a', '--aircrack',
                        help='Launch aircrack-ng attack on wireless network',
                        action='store_true')

    parser.add_argument('-sp', '--spyder',
                        help='Enable web crawling and information gathering mode',
                        action='store_true')

    args = parser.parse_args()

    if args.viewer:
        if args.code:
            site_name = args.viewer.split('//')[1].split('/')[0]
            output_dir = f'output/view code source/{site_name}'
            os.makedirs(output_dir, exist_ok=True)
            os.system(f'python ./programs/viewer.py {args.viewer} --save {output_dir} --info')
        else:
            os.system(f'python ./programs/viewer.py {args.viewer} --info')
            
    elif args.sniff:
        if not args.file:
            print("Error: Output file (-f) required for sniffing mode")
            sys.exit(1)
        os.system(f'python ./programs/sniffer.py -o {args.file}')
            
    elif args.cracker:
        if not args.username:
            print("Error: Username (-u) required for cracking mode")
            sys.exit(1)
        os.system(f'python ./programs/cracker.py {args.cracker} {args.username} -m {args.min} -max {args.max}')

    elif args.aircrack:
        os.system('python ./programs/aircrack.py')

    elif args.spyder:
        os.system('python ./programs/spyder.py')
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
