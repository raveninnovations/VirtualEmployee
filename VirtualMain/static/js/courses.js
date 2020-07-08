// var state_arr = new Array("MCA", "MBA", "BE/BTECH", "M.COM", "MSC","MSW",  "MA", "LLM", "M.Arch", "MBE" , "MDS", "MHM" , "MHRM", "M.Phil", "MS","MPA", "MEd", "MJ", "MMS", "M.Tech");

var state_arr = new Array("Higher School", "Associate Degree" , "Bachelors", "Masters", "Doctoral Degree");


var s_a = new Array();
s_a[0]="";
s_a[1]=" Science (Biology) | Science (Computer) | Commerce (With Maths) | Commerce (Without Maths) | Arts ";
s_a[2]=" Administration of Justice |  Advertising | Architectural Building Engineering Technology | Art | Aviation Mechanics | Digital Media | English | Environmental Science | Environmental Studies | General Psychology | Music | Applied Science in Accounting Specialist | Applied Science in Baking and Pastry | Applied Science in Business Administration | Applied Science in Business Administration - Finance | Applied Science in Computer Applications | Applied Science in Computer Game Design | Applied Science in Computer Information Systems | Applied Science in Telecommunications Technology | Arts in Computer Information Systems | Biotechnology | Science in Computer Information Science | Science in Computer Science | Arts and science | Others";
s_a[3]="  Architecture | Biochemistry | Business Administration | Commerce | Computer Applications | Computer Information Systems | Economics | Engineering | Fine Arts | Genetic Engineering and Biotechnology | Information Systems | Management | Music | Pharmacy |  Technology in  Aeronautical Engineering | Technology in Automobile Engineering |  Technology in Biotechnology | Technology in Civil Engineering | Technology in Computer Science and Engineering | Technology in Electrical and Electronics Engineering | Technology in Mechanical Engineering | Technology in Electronics & Communication | Accountancy | Arts in Biology | Arts in Communication | Science in Accountancy | Computer Science Engineering |  Science in Business and Technology | Others";
s_a[4]=" Accountancy | Accounting and Information Systems | Applied Finance | Applied Science | Architecture |  Arts | Biotechnology | Business Administration | Business Administration Management of Technology | Business | Business Economics | Computational Finance | Computer Applications | Computer Science | Design | Economics | Educational Technology | Engineering | Finance | Fine Arts | International Affairs | Management | Mathematics | Medical Science | Music | Network and Communications Management |  Pharmacy | Science | Science in Computing Research | Science in Information Technology | Others";
s_a[5]=" Arts | Business Administration | Commerce | Dental Surgery | Education | Engineering | Fine Arts | Health Administration | Health Science | Law | Liberal Studies | Management | Medicine | Ministry | Musical Arts | Pharmacy | Philosophy | Public Administration | Science | Theology | Others";





// var s_a = new Array();
//
// s_a[0]="";
//
// s_a[1]=" Computer Science | Computer Application | Systems Management | Systems Development | Hardware Technology";
//
// s_a[2]=" Human Resource Management | Information Technology | Marketing Management | Finance | Logistics Management | Marketing Management| Business Management | Rural Management | Health Care Management | Operations Management | Event Management";
//
// s_a[3]=" Automobile Engineering | Robotics and Automation | Environmental Science | Geospatial Science | Materials Science";
//
// s_a[4]="Finance | Marketing | Human Resource Management | International Business Operations | Accounting | Economics | Statistics";
//
// s_a[5]=" Computer Science | Finance | Marketing | Information Technology | Management | Economics | Mental Healthcare | Psychology | Business | Mechanical Engineering | Biology | Accounting | Engineering | Information System | Data Science";
//
// s_a[6]=" Human Resource Management | Criminology and Correctional Administration | Medical and Psychiatric Social Work | Family and Child Welfare | Rural and Urban Community Development and Schools Social Work | Medical and Psychiatric Social Work | Urban and Rural Community Development | Personnel Management | Industrial Relations & Labour Welfare";
//
// s_a[7]=" English | Political Science | Philosophy | Education | Area Studies | Teaching | International Relations | Media | Culture Studies | Theology | Communications | History | Film Studies | Mental Healthcare | Economics | Psychology";
//
// s_a[8]=" Business Law | Criminal Law | Intellectual Property Rights | Corporate Law | Constitutional Law | Human Rights | International Law | Labour Laws";
//
// s_a[9]=" Architectural Conservation | Architecture and Construction Project Management | Computer Aided Architectural Design | Digital Architecture | Environmental Architecture | Interior Architecture | International Architecture | Landscape Architecture | Rural Architecture | Sustainable Architecture | Town and Country Planning | Transportation Planning and Design | Urban and Regional Planning | Urban Design | Valuation and Arbitration";
//
// s_a[10]=" Corporate Finance | Portfolio Management | Agriculture Economics |Advanced Econometrics | Financial Risk Management | Energy Economics | Game Theory and Application | Time Series and Business Forecasting | Labour Economics | Managing Change in Organisations";
//
// s_a[11]=" Public Health Dentistry | Oral Pathology and Microbiology | Oral Medicine and Radiology | Periodontology | Conservative Dentistry and Endodontics | Oral and Maxillofacial Surgery | Orthodontics and Dentofacial Orthopaedics | Prosthodontics | Pedodontics | Preventive dentistry";
//
// s_a[12]=" Hospital management | healthcare administration | health services administration";
//
// s_a[13]=" Finance | Marketing | Systems";
//
// s_a[14]="History | English | Political Science | Economics | Sociology | Public Administration | Social Work | Biology | Computer Science | Commerce | Law | Education | Geography | Human Developmental Studies";
//
// s_a[15]=" Biomedical Engineering | Chemical Engineering | Statistics | Operations Research Analyst | Computer and Information Technology | Management Information Systems | Environmental Engineering | Systems Engineering | Computer Engineering | Mathematics";
//
// s_a[16]=" Music | Dance | Theatre";
//
// s_a[17]=" General Surgery | Pediatrics | Obstetrics & Gynecology |  Dermatology | Ophthalmology | Orthopedics | ENT (Ear, Nose and Throat) | Psychiatry | Anesthesiology";
//
// s_a[18]=" Radio and TV Journalism | Print Journalism And New Media | Photojournalism | Digital Journalism | Event Management | Social Media |Advertisement and Public Relations";
//
// s_a[19]=" Finance | Operations | Business | Marketing | Human Resource | Systems";
//
// s_a[20]=" Civil Engineering | Computer Science and Engineering | Chemical Engineering | Electrical Engineering | VLSI | Mechanical Engineering | Electronics and Communication Engineering";


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

option_str.length=0; // Fixed by Julian Woods

option_str.options[0] = new Option('Select Specialization','');

option_str.selectedIndex = 0;

var city_arr = s_a[city_index].split("|");

for (var i=0; i<city_arr.length; i++) {

option_str.options[option_str.length] = new Option(city_arr[i],city_arr[i]);

}

}
