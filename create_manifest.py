# --- Building Manifest Files --- #
import json
import glob
import os
import librosa
import re
import sys

"""
LibriSpeech
  train
    84
      121123
        84-121123.trans.txt
        84-121123-0000.flac
        84-121123-0001.flac
        84-121123-0002.flac
        ...
"""

# Function to build a manifest
def build_manifest(transcript_list, manifest_path, data_path):
    with open(manifest_path, "w") as fout:
        for transcript_path in transcript_list:
            with open(transcript_path, "r") as fin:
                for line in fin:
                    pattern = re.compile(
                        r"(?P<file_id>\d+\-\d+\-\d+)(?P<transcript>.+)"
                    )
                    match = pattern.match(line)

                    # Lines look like this:
                    #   fileID transcript
                    transcript = match["transcript"].lower().strip()

                    file_id = match["file_id"]  # e.g. "116-288045-0001"
                    audio_path = os.path.join(
                        data_path,
                        file_id[: file_id.find("-")],
                        file_id[file_id.find("-") + 1 : file_id.rfind("-")],
                        file_id + ".wav",
                    )

                    duration = librosa.core.get_duration(path=audio_path)

                    # Write the metadata to the manifest
                    metadata = {
                        "audio_filepath": audio_path,
                        "duration": duration,
                        "text": transcript,
                    }
                    json.dump(metadata, fout)


def main():
    args = sys.argv[1:]

    librispeech_path = "./LibriSpeech"

    if len(args) >= 1:
        if os.path.exists(args[0]):
            librispeech_path = args[0]
        else:
            raise FileNotFoundError(args[0])

    # Building Manifests
    train_clean_transcript_list = glob.glob(
        librispeech_path + "/train/dev-clean/**/*.trans.txt", recursive=True
    )
    train_clean_manifest = librispeech_path + "/train_clean_manifest.json"
    train_path = librispeech_path + "/train/dev-clean"
    if not os.path.isfile(train_clean_manifest):
        build_manifest(train_clean_transcript_list, train_clean_manifest, train_path)
        print("Train clean manifest created.")
    else:
        print("Train clean exists.")

    train_other_transcript_list = glob.glob(
        librispeech_path + "/train/dev-other/**/*.trans.txt", recursive=True
    )
    train_other_manifest = librispeech_path + "/train_other_manifest.json"
    train_path = librispeech_path + "/train/dev-other"
    if not os.path.isfile(train_other_manifest):
        build_manifest(train_other_transcript_list, train_other_manifest, train_path)
        print("Train other manifest created.")
    else:
        print("Train other exists.")

    test_clean_transcript_list = glob.glob(
        librispeech_path + "/test/test-clean/**/*.trans.txt", recursive=True
    )
    test_clean_manifest = librispeech_path + "/test_clean_manifest.json"
    test_path = librispeech_path + "/test/test-clean"
    if not os.path.isfile(test_clean_manifest):
        build_manifest(test_clean_transcript_list, test_clean_manifest, test_path)
        print("Test clean manifest created.")
    else:
        print("Test clean exists.")

    test_other_transcript_list = glob.glob(
        librispeech_path + "/test/test-other/**/*.trans.txt", recursive=True
    )
    test_other_manifest = librispeech_path + "/test_other_manifest.json"
    test_path = librispeech_path + "/test/test-other"
    if not os.path.isfile(test_other_manifest):
        build_manifest(test_other_transcript_list, test_other_manifest, test_path)
        print("Test other manifest created.")
    else:
        print("Test other exists.")


if __name__ == "__main__":
    main()
