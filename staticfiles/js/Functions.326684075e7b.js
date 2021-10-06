const chgPort=document.querySelector("#chgPort");

chgPort.addEventListener('click',getPort('{{x}}'));

function getPort(id){
    var domain_name=id;
    $.ajax({
        type: "GET",
        url: "test/",
        data: domain_name,
        success: function (result) {
            alert(result)
        }
    })
}