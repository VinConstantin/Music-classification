const MAXQTN = 8;
const MINQTN = 2;
function plusQuantite(id) {
    let val = parseInt($("#" + id).data("quantite"))
    if($("#" + id).data("quantite")<MAXQTN){
        $("#" + id).data("quantite",val+1);   
        $("#" + id).html(val+1);    
    }
}
function moinsQuantite(id) {
    let val = parseInt($("#" + id).data("quantite"))
    if($("#" + id).data("quantite")>MINQTN){
        $("#" + id).data("quantite",val-1);   
        $("#" + id).html(val-1);    
    }
}
function insertCbBtn(row,newRow, i){

    let newCell = newRow.insertCell(i)
    let div = document.createElement("div")
    div.className="input-group"
    div.style.minWidth="120px"

    let cb = document.createElement("input");
    cb.setAttribute("type", "checkbox");  
    cb.className = "form-control cb"
    cb.style.maxWidth = "40px"
    cb.id=`cb${i}`
    div.appendChild(cb)

    let input = document.createElement("input");
    input.className = "form-control"
    input.style.maxHeight = "40px"
    input.value = row==null?"": row.data[0][i];
    input.id=`tb`
    div.appendChild(input)

    newCell.appendChild(div)
}

function lireCsv(){
    document.getElementById("Importer").disabled = true;
    document.getElementById("1").style.display = "none";
    document.getElementById("2").style.display = "block"

    let file = customFile.files[0]
    let nb = 0;
    let length = 0;
    let tableHead = document.getElementById("table").getElementsByTagName('thead')[0];
    let tableBody = document.getElementById("table").getElementsByTagName('tbody')[0];
    let newCell
    let newRow
    Papa.parse(file, {
        step: function(row) {
            nb++
            length = row.data[0].length
            if(nb == 1){
                if(document.getElementById('gridCheck1').checked){
                    newRow = tableHead.insertRow(-1)
                    for(let i = 0; i < length;i++){
                        insertCbBtn(row,newRow, i)
                    }
                }
                else{
                    newRow = tableHead.insertRow(-1)
                    for(let i = 0; i < length;i++){
                        insertCbBtn(null,newRow, i)
                    }
                    newRow = tableBody.insertRow(-1)
                    for(let i = 0; i < length;i++){
                        newCell = newRow.insertCell(i)
                        newCell.innerHTML = row.data[0][i]
                    }
                }
            }
            else{
                newRow = tableBody.insertRow(-1)
                for(let i = 0; i < length;i++){
                    newCell = newRow.insertCell(i)
                    newCell.innerHTML = row.data[0][i]
                }
            }          
        },
        complete: function() {
            console.log("All done!");
        }
    });
    
}
function convertHtmlTableToArrayJQERRY(tableId){
    let array = [];
    let headers = [];
    let tb
    let cb
    $(`#${tableId} thead div`).each(function(index, item) {
        tb = item.querySelector("#tb")
        cb = item.querySelector(".cb")
        if(cb.checked || tb.value === "target")
            headers[index] = tb.value
    });
    $(`#${tableId} tbody tr`).has('td').each(function() {
        let arrayItem = {};
        $('td', $(this)).each(function(index, item) {
            if(headers[index]!=null)
            arrayItem[headers[index]] = $(item).html().replace("$","");
        });
        array.push(arrayItem);
    });
    return array;
}
function convertHtmlTableToArray(tableId){
    let array = [];
    let headers = [];
    let tb
    let cb
    $(`#${tableId} thead div`).each(function(index, item) {
        tb = item.querySelector("#tb")
        cb = item.querySelector(".cb")
        if(cb.checked || tb.value === "target")
            headers[index] = tb.value
    });
    let body = document.getElementById("tableBody")
    for (let i = 0, row; row = body.rows[i]; i++) {
        let arrayItem = {};
        for (let j = 0, col; col = row.cells[j]; j++) {
            if(headers[j]!=null)
            arrayItem[headers[j]] = col.textContent.replace("$","");
            console.log(arrayItem)
        }
        array.push(arrayItem);
    }

    return array;
}
function sendData(){
    document.getElementById("btnBuild").disabled = true
    show(document.getElementById("loading"))

    let tableId = `table`
    let array = convertHtmlTableToArray(tableId)
    $.ajax({
        type: "POST",
        url: "constructModel",
        data: JSON.stringify(array),
        success: function( data, textStatus, jQxhr ){
            document.getElementById("2").style.display = "none";
            document.getElementById("3").style.display = "block";
            buildForm(data)

            console.log(data)
            console.log(textStatus)
        },
        error: function( jqXhr, textStatus, errorThrown ){
            console.log( jqXhr );
            console.log( textStatus );
            console.log( errorThrown );
        },
        contentType: 'application/json',
      });
}

function buildForm(data){
    let div = document.getElementById("divTb")
    let form = document.getElementById('classifier');
    let childDiv
    let label
    let array = data["columns"]
    let input
    array.forEach(element => {
        if(element != "target"){
            childDiv = document.createElement("div")
            childDiv.classList = "form-group"
            label = document.createElement("label")
            label.innerText = element
            input = document.createElement('input');
            input.type = "text"
            input.id = element
            input.name = element
            input.style="min-width: 300px"
            input.className = "form-control"
            input.placeholder = element
            form.appendChild(input)
            childDiv.appendChild(label)
            childDiv.appendChild(input)
            div.appendChild(childDiv)
        }
    });

    let btn = document.createElement("button")
    btn.onclick = function(){
        Classifier();
    };
    btn.className = "btn btn-primary"
    btn.innerText = "Classifier"
    btn.type = "button"

    div.appendChild(btn)
}

function Classifier(){
    const form = document.getElementById('classifier');

    const data = ConvertFormToJSON(form);
    console.log("send")
    console.log(data)
    $.ajax({
        type: "POST",
        url: "classifier",
        data: JSON.stringify(data),
        success: function( data, textStatus, jQxhr ){
             document.getElementById("resultSuccess").innerHTML = `Cet objet est de classe : ${data}!`;
             hide(document.getElementById("alertError"));
             show(document.getElementById("alertSuccess"));
         
        },
        error: function( jqXhr, textStatus, errorThrown ){
            //Error
           document.getElementById("resultError").innerHTML = `Une erreur est survenue`;
           hide(document.getElementById("alertSuccess"));
           show(document.getElementById("alertError"));
           
           console.log(jqXhr)
           console.log(textStatus)
           console.log(errorThrown)
        },
        contentType: 'application/json',
      });
}

function ConvertFormToJSON(form){
    var array = jQuery(form).serializeArray();
    var json = {};
    
    jQuery.each(array, function() {
        json[this.name] = this.value || '';
    });
    
    return json;
}

// Show an element
function show(elem) {
    elem.style.display = 'block';
};

// Hide an element
function hide(elem) {
    elem.style.display = 'none';
};