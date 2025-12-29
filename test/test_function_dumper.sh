cd /Users/jakerase/Desktop/projects/compyler/build
#!/bin/bash
// Source - https://stackoverflow.com/a
// Posted by Mike Müller, modified by community. See post 'Timeline' for change history
// Retrieved 2025-12-29, License - CC BY-SA 4.0
// Modified 2025-12-29 by Jake Rase
python -c 'import dis; from importable import test_function; dis.dis(test_function)' > ../test/test_function.csv

