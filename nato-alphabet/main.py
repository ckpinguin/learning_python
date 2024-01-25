import pandas
""" student_dict = {
    "student": ["Angela", "James", "Lily"],
    "score": [56, 76, 98]
}

# Looping through dictionaries:
for (key, value) in student_dict.items():
    # Access key and value
    pass

student_data_frame = pandas.DataFrame(student_dict)

# Loop through rows of a data frame
for (index, row) in student_data_frame.iterrows():
    # Access index and row
    # Access row.student or row.score
    pass """

# Keyword Method with iterrows()
# {new_key:new_value for (index, row) in df.iterrows()}

# {"A": "Alfa", "B": "Bravo"}
df = pandas.read_csv('nato_phonetic_alphabet.csv')
# print(df)
# df_dict = df.to_dict()
# print(df_dict)
alphabet_dict = {row.letter: row.code for (_, row) in df.iterrows()}
# print(alphabet_dict)


def get_input():
    word = input('Enter a name: ').upper()
    return word


def translate_to_nato(chars):
    try:
        output_list = [alphabet_dict[letter] for letter in chars]
        return output_list
    except KeyError:
        print("Sorry, only letters allowed.")
        return translate_to_nato(get_input())


output_list = translate_to_nato(get_input())
print(output_list)
