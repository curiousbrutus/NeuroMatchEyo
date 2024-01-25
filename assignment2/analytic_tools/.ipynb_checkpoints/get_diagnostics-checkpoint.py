{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "ea3ef5ad-77db-46bc-b4da-edeb08b9864d",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "{'Total number of files': 7, 'Total number of subdirectories': 2, 'Total number of .csv files': 0, 'Total number of .txt files': 0, 'Total number of .npy files': 0, 'Total number of .md files': 0, 'Total number of other files': 7}\n"
     ]
    }
   ],
   "source": [
    "import os\n",
    "from pathlib import Path\n",
    "from typing import Dict\n",
    "\n",
    "def get_diagnostics(dir: str | Path) -> Dict[str, int]:\n",
    "    \"\"\"Get diagnostics for the directory tree, with the root directory pointed to by dir.\n",
    "       Counts up all the files, subdirectories, and specifically .csv, .txt, .npy, .md, and other files in the whole directory tree.\n",
    "\n",
    "    Parameters:\n",
    "        dir (str or pathlib.Path): Absolute path to the directory of interest\n",
    "\n",
    "    Returns:\n",
    "        res (Dict[str, int]): a dictionary of the findings with the following keys: files, subdirectories, .csv files, .txt files, .npy files, .md files, other files.\n",
    "\n",
    "    \"\"\"\n",
    "    # Dictionary to store counts\n",
    "    res = {\n",
    "        \"files\": 0,\n",
    "        \"subdirectories\": 0,\n",
    "        \".csv files\": 0,\n",
    "        \".txt files\": 0,\n",
    "        \".npy files\": 0,\n",
    "        \".md files\": 0,\n",
    "        \"other files\": 0,\n",
    "    }\n",
    "\n",
    "    try:\n",
    "        # Ensure the provided path is a valid directory\n",
    "        dir = Path(dir)\n",
    "        if not dir.is_dir():\n",
    "            raise NotADirectoryError(f\"'{dir}' is not a valid directory.\")\n",
    "\n",
    "        # Use pathlib's rglob method to traverse the directory tree\n",
    "        for file_path in dir.rglob('*'):\n",
    "            if file_path.is_file():\n",
    "                res[\"files\"] += 1\n",
    "                # Check the file extension and increment the respective count\n",
    "                file_extension = file_path.suffix.lower()\n",
    "                if file_extension == '.csv':\n",
    "                    res[\".csv files\"] += 1\n",
    "                elif file_extension == '.txt':\n",
    "                    res[\".txt files\"] += 1\n",
    "                elif file_extension == '.npy':\n",
    "                    res[\".npy files\"] += 1\n",
    "                elif file_extension == '.md':\n",
    "                    res[\".md files\"] += 1\n",
    "                else:\n",
    "                    res[\"other files\"] += 1\n",
    "            elif file_path.is_dir():\n",
    "                res[\"subdirectories\"] += 1\n",
    "\n",
    "        return res\n",
    "\n",
    "    except TypeError:\n",
    "        raise TypeError(\"Input must be a path-like object.\")\n",
    "    except NotADirectoryError as e:\n",
    "        raise NotADirectoryError(f\"{e}\")\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "eda96dd0-16a9-4e45-a889-5ffff2203e43",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "mlsimone",
   "language": "python",
   "name": "mlsimone"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
