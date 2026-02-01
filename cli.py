import argparse
from steganography import ImageSteganography

def main():
    parser = argparse.ArgumentParser(description='Image Steganography Tool')
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Encode command
    encode_parser = subparsers.add_parser('encode', help='Encode a message into an image')
    encode_parser.add_argument('-i', '--input', required=True, help='Input image path')
    encode_parser.add_argument('-o', '--output', required=True, help='Output image path')
    encode_parser.add_argument('-m', '--message', required=True, help='Secret message')
    encode_parser.add_argument('-b', '--bits', type=int, default=1, choices=[1,2,3,4], 
                              help='Number of LSBs to use (default: 1)')
    
    # Decode command
    decode_parser = subparsers.add_parser('decode', help='Decode a message from an image')
    decode_parser.add_argument('-i', '--input', required=True, help='Encoded image path')
    decode_parser.add_argument('-b', '--bits', type=int, default=1, choices=[1,2,3,4],
                              help='Number of LSBs used (default: 1)')
    
    # Info command
    info_parser = subparsers.add_parser('info', help='Get image information and capacity')
    info_parser.add_argument('-i', '--input', required=True, help='Image path')
    info_parser.add_argument('-b', '--bits', type=int, default=1, choices=[1,2,3,4],
                            help='Number of LSBs to calculate for (default: 1)')
    
    args = parser.parse_args()
    
    stego = ImageSteganography()
    
    if args.command == 'encode':
        stego.set_bits_used(args.bits)
        stego.encode_image(args.input, args.message, args.output)
        print(f"Message encoded successfully into {args.output}")
        
    elif args.command == 'decode':
        stego.set_bits_used(args.bits)
        message = stego.decode_image(args.input)
        print(f"Decoded message: {message}")
        
    elif args.command == 'info':
        stego.set_bits_used(args.bits)
        info = stego.calculate_capacity(args.input)
        print(f"Image Information:")
        print(f"  Dimensions: {info['image_dimensions'][0]}x{info['image_dimensions'][1]}")
        print(f"  Channels: {info['channels']}")
        print(f"\nCapacity with {args.bits} LSB(s):")
        print(f"  Bits: {info['bits']}")
        print(f"  Bytes: {info['bytes']}")
        print(f"  Characters: {info['characters']}")
        
    else:
        parser.print_help()

if __name__ == "__main__":
    main()