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

# Link to VTE issue
ln -s /etc/profile.d/vte-2.91.sh /etc/profile.d/vte.sh
