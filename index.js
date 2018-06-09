function updateMetaData(data){
	var PANEL = document.getElementById("sample-metadata");
	PANEL.innerHTML='';
	for (var key in data){
		h6tag = document.createElement("h6");
		h6Text = document.createTextNode('${key}: ${data[key]}');
		h6tag.append(h6Text);
		PANEL.appendChild(h6tag);
	}
}

function buildCharts(sampleData, otuData){
	var labels = sampleData[0]['otu_ids'].map(function(item){
		return otuData[item]
	});
	var bubblelayout = {
		margin:{t:0},
		hovermode: 'closet',
		xaxis: {title: "OTU ID"}
	};
	var bubbleData = [{
		x: sampleData[0]['otu_ids'],
		y: sampleData[0]['sample_values'],
		text: labels,
		mode: 'markers',
		marker: {
			size: sampleData[0]['sample_values'],
			color: sampleData[0]['otu_ids'],
			colorscale: "Earth"
		}
	}];
	var BUBBLE = document.getElementById('bubble');
	Plotly.plot(BUBBLE, bubbleData, bubblelayout);
	console.log(sampleData[0]['sample_values'].slice(0,10))
	var pieData = [{
		values: sampleData[0]['sample_values'].slic(0,10),
		labels: sampleData[0]['otu_ids'].slice(0,10),
		hovertext: labels.slice(0,10),
		hoverinfo: 'hovertext',
		type: 'pie'
	}];
	var pielayout = {
		margin: {t:0, l:0}
	};
	var PIE = document.getElementById('pie');
	Plotly.plot(PIE, pieData, pielayout);
};

function updateCharts(sampleData, otuData){
	var sampleValues = sampleData[0]['sample_values'];
	var otuIDs = sampleData[0]['otu_ids'];
	var labels = otuIDs.map(function(item){
		return otuData[item]
	});

	var BUBBLE = document.getElementById('bubble');
	Plotly.restyle(BUBBLE, 'x', [otuIDs]);
	Plotly.restyle(BUBBLE, 'y', [sampleValues]);
	Plotly.restyle(BUBBLE, 'text', [labels]);
	Plotly.restyle(BUBBLE, 'marker.size', [sampleValues]);
	Plotly.restyle(BUBBLE, 'marker.color', [otuIDs]);

	var PIE = document.getElementById('pie')
	var pieUpdate = {
		values: [sampleValues.slice(0,10)],
		lables: [otuIDs.slice(0,10)],
		hovertext: [labels.slice(0,10)],
		hoverinfo: 'hovertext',
		type: 'pie'
	};
	Plotly.restyle(PIE, pieUpdate);
}

function getData(sample, callback){
	Plotly.d3.json(`/samples/${sample}`, function(error, sampleData){
		if (error) return console.warn(error);
		Plotly.d3.json('/otu'), function(error, otuData){
			if (error) return console.warn(error);
			callback(sampleData,otuData);
		};
	});
	Plotly.d3.json(`/metadata/${sample}`, function(error, metaData){
		if (error) return console.warn(error);
		updateMetaData(metaData);
	});
}
