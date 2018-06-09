import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc
from flask import Flask, jsonify

import pandas as pd 
import numpy as np 

engine = create_engine("sqlite:///belly_button_biodiversity.sqlite")

Base=automap_base()
Base.prepare(engine, reflect=True)

OTU = Base.classes.otu 
Samples = Base.classes.samples 
Metadata = Base.classes.metadata 

session = Session(engine)

app = Flask(__name__)

@app.route("/")
def home():
	return(
		f"Welcome to the Belly Button Biodiversity API </br>"
		f"Available Routes: </br>"
		f"/api/v1.0/names</br>"
		f"/api/v1.0/otu</br>"
		f"/api/v1.0/metadata/<samples></br>"
		f"/api/v1.0/wfreq/<samples></br>"
		f"/api/v1.0/sample/<samples></br>")

@app.route("/names")
def sample_names():
	samples=session.query(Samples).statement
	df = pd.read_sql_query(samples,session.bind)
	df.set_index('otu_id', inplace=True)
	return jsonify(list(df.columns))

@app.route("/otu")
def otu_data():
	results = session.query(OTU.lowest_taxonomic_unit_found).all()
	otu_data = list(np.ravel(results))
	return jsonify(otu_data)

@app.route("/metadata/<samples>")
def metadata_route(sample):
	num_sample = sample.replace("BB_", "")
	metadata_sample = session.query(Metadata.AGE, Metadata.BBTYPE, Metadata.ETHNICITY, Metadata.GENDER, Metadata.LOCATION, Metadata.SAMPLEID).filter_by(SAMPLEID=num_sample).all()
	record = metadata_sample[0]
	metadata_dict = {"Age":record[0], "BB_Type": record[1], "Ethnicity": record[2], "Gender": record[3], "location": record[4], "Sample_ID": record[5]}
	return metadata_dict

	sample_result = metadata_route("BB_940")
	return jsonify(sample_result)

@app.route("/wfreq/<samples>")
def wfreq_route(sample):
	num_w_sample = sample.replace("BB_", "")
	wfreq_sample = session.query(Metadata.SAMPLEID, Metadata.WFREQ).filter_by(SAMPLEID = num_w_sample).all()
	w_record = wfreq_sample[0]
	wfreq_dict = {"Sample ID": w_record[0], "Wash Frequency": w_record[1]}
	wfrequency = wfreq_dict["Wash Frequency"]
	return wfrequency

	wfreq_results = wfreq_route("BB_940")
	return jsonify(wfreq_results)

@app.route("/sample/<sample>")
def otu_sample_values(sample):
	stmt = session.query(Samples).statement
	df = pd.read_sql_query(stmt, session.bind)
	if sample not in df.columns:
		return jsonify(f"ERROR ERROR")
	df = df[df[sample]>1]
	df = df.sort_values(by=sample, ascending=0)
	data = [{
		"otu_ids": df[sample].index.values.tolist(),
		"sample_values": df[sample].values.tolist()
	}]
	return jsonify(data)
if __name__ == "__main__":
	app.run(debug=True)







		
