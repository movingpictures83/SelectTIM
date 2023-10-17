
# The purpose of this script is to select TIM and AMP/MEM cohorts

import pandas as pd

def get_cohort(row):
    if row['r_Ticarcillin-Clavulanate']>0:
        return 'TIM'
    elif row['r_Ampicillin']>0 or row['r_Meropenem']:
        return 'AMP/MEM'
    else:
        return 'Other'

class SelectTIMPlugin:
 def input(self, inputfile):
  self.df = pd.read_csv(inputfile)#('./analysis-out/4-Select_major_ABR/PTR_species_filtered_metadata_major_AMR_RPKM.csv')

 def run(self):
     pass

 def output(self, outputfile):
     self.df['Treatment'] = self.df.apply(lambda row: get_cohort(row), axis=1)

     self.df = self.df[self.df['Treatment']!='Other']

     print("Number of samples in TIM cohort: {}".format(len(self.df[self.df['Treatment']=='TIM'])))
     print("Number of samples in AMP/MEM cohort: {}".format(len(self.df[self.df['Treatment']=='AMP/MEM'])))

     ABR_genes = [x for x in self.df.columns if 'ARO' in x]

     self.df = self.df[['Treatment'] + ABR_genes]

     for gene in ABR_genes:
      if self.df[gene].mean() == 0:
        self.df = self.df.drop(gene, axis=1)

     self.df.to_csv(outputfile, index=False)
     #self.df.to_csv('analysis-out/4-Select_major_ABR/abr_tim.csv', index=False)
