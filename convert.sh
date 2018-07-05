if [[ $1 -eq 0 ]];
then
    echo "Error: no positional arguments"
    exit 1
fi

pandoc -f gfm -t html $1.md #| python convert.py
