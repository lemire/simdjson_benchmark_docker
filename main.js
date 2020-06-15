// return a json object from a local file
function load_json(filename) {
	let req = new XMLHttpRequest();
	req.overrideMimeType("application/json");
	req.open("GET", filename, false);
	req.send();
	if(req.status == 200) return JSON.parse(req.responseText);
	else return null;
}

function get_commits(jsons) {
	commits_arr = [];
	for(j of jsons) {
		for(c in j) {
			if(commits_arr.indexOf(c) == -1) commits_arr.push(c);
		}
	}
	return commits_arr;
}

function date_data_array(jsons) {
	
}

function commit_data_array(jsons, benchnames) {
	var arr = [["Commit"]];
	for(bn of benchnames) {
		arr[0].push(bn);
	}

	for(c of get_commits(jsons)) {
		row = [c];
		for(let i = 0; i < jsons.length; i++) {
			if(jsons[i][c].speed != null) row[i + 1] = jsons[i][c].speed;
			else row[i + 1] = 0;
		}
		arr.push(row);
	}

	return arr;
}
