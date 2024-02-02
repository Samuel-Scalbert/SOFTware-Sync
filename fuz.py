def extract_substring_with_offsets(context, offset_start, offset_end):
    return context[offset_start:offset_end]

# Example usage
context_string = "The input for MODELLER consisted of the aligned sequences of 1gcc and the SiDREB2, a steering file that gives all the necessary commands to the MODELLER to produce a homology model of the target on the basis of its alignment with the template."

offset_start = 144
offset_end = 152

extracted_substring = extract_substring_with_offsets(context_string, offset_start, offset_end)
print(extracted_substring)
