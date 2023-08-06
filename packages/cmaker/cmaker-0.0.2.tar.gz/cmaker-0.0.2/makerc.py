#!/usr/bin/python3

if __name__ == "__main__":
    
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--config", default="cmaker.config")
    args = parser.parse_args()
    
    from cmaker.maker import Maker
    
    maker = Maker(args.config)
    maker.make(args.input, args.output)
