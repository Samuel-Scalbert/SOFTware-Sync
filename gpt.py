import requests
import g4f

p_tag = '<p>Sequencing of the recombinant plasmids and the PCR amplification products was performed according to <ref type="bibr" target="b26">Lata et al. (2010)</ref>. Alignments were carried out by ClustalW with default parameters <ref type="bibr" target="#b51">(Thompson et al., 1994)</ref>. The phylogenetic tree for the SiDREB2 gene was built using the software program MEGA 4.0 based on protein sequences. The phylogenetic tree was set up with the distance matrix using the Neighbor-Joining (NJ) method with 1000 bootstrap replications.</p>'
context = 'Alignments were carried out by ClustalW with default parameters <ref type="bibr" target="#b51">(Thompson et al.'
list = [p_tag,context]

g4f.debug.logging = True  # Enable debug logging
g4f.debug.version_check = False  # Disable automatic version checking
print(g4f.Provider.Bing.params)  # Print supported args for Bing

# Using automatic a provider for the given model
## Streamed completion
response = g4f.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello"}],
    stream=True,
)
for message in response:
    print(message, flush=True, end='')

## Normal response
response = g4f.ChatCompletion.create(
    model=g4f.models.gpt_4,
    messages=[{
    "model": "gpt-3.5-turbo-16k",
    "stream": False,
     "messages" : [
       {"role": "user", "content": ['<p>Sequencing of the recombinant plasmids and the PCR amplification products was performed according to <ref type=\"bibr\" target=\"b26\">Lata et al. (2010)</ref>. Alignments were carried out by ClustalW with default parameters <ref type=\"bibr\" target=\"#b51\">(Thompson et al., 1994)</ref>. The phylogenetic tree for the SiDREB2 gene was built using the software program MEGA 4.0 based on protein sequences. The phylogenetic tree was set up with the distance matrix using the Neighbor-Joining (NJ) method with 1000 bootstrap replications.</p>', 'Alignments were carried out by ClustalW with default parameters <ref type=\"bibr\" target=\"#b51\">(Thompson et al.']},
    ]
}],
)  # Alternative model setting

print(response)