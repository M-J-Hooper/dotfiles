#!/bin/bash

DIR="$( cd "$(dirname "$0")" ; pwd -P )"
cd $DIR

for FILE in .[!.]*; do
    if [ $FILE != ".git" ]; then
        if ln -sf "$DIR/$FILE" "$HOME"; then
            echo "$HOME/$FILE -> $FILE"
        else
            echo "Could not create link for $FILE"
        fi
    fi
done

# Manual linking
ln -sf "$DIR/karabiner.json" "$HOME/.config/karabiner"
