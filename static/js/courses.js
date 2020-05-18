var state_arr = new Array("MCA", "MBA", "Arunachal Pradesh", "M.COM", "MSC", "BE/BTECH", "Chhattisgarh", "Dadra & Nagar Haveli", "Daman & Diu", "Delhi", "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jammu & Kashmir", "Jharkhand", "Karnataka", "Kerala", "Lakshadweep", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Orissa", "Pondicherry", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Tripura", "Uttar Pradesh", "Uttaranchal", "West Bengal");

var s_a = new Array();
s_a[0]="";
s_a[1]=" Computer Science ";
s_a[2]=" Human Resource Management | Information Technology | Marketing Management | Finance ";
s_a[3]=" ";
s_a[4]=" ";
s_a[5]=" ";
s_a[6]=" Chandigarh | Mani Marja";
s_a[7]=" ";
s_a[8]=" ";
s_a[9]=" ";
s_a[10]=" ";
s_a[11]=" ";
s_a[12]=" ";
s_a[13]=" ";
s_a[14]=" ";
s_a[15]=" ";
s_a[16]=" ";
s_a[17]=" ";
s_a[18]=" ";
s_a[19]=" ";
s_a[20]=" ";
s_a[21]="";
s_a[22]=" ";
s_a[23]="";
s_a[24]=" ";
s_a[25]=" ";
s_a[26]=" ";
s_a[27]=" ";
s_a[28]=" ";
s_a[29]=" ";
s_a[30]=" ";
s_a[31]=" ";
s_a[32]=" ";
s_a[33]="";
s_a[34]="  ";
s_a[35]=" ";

function print_state(state_id){
	// given the id of the <select> tag as function argument, it inserts <option> tags
	var option_str = document.getElementById(state_id);
	option_str.length=0;
	option_str.options[0] = new Option('Select Course','');
	option_str.selectedIndex = 0;
	for (var i=0; i<state_arr.length; i++) {
		option_str.options[option_str.length] = new Option(state_arr[i],state_arr[i]);
	}
}

function print_city(city_id, city_index){
	var option_str = document.getElementById(city_id);
	option_str.length=0;	// Fixed by Julian Woods
	option_str.options[0] = new Option('Select Specialization','');
	option_str.selectedIndex = 0;
	var city_arr = s_a[city_index].split("|");
	for (var i=0; i<city_arr.length; i++) {
		option_str.options[option_str.length] = new Option(city_arr[i],city_arr[i]);
	}
}

