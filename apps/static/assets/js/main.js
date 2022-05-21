
console.log('loaded main js')

fetch('/config/')
.then((result) =>{
    return result.json();
})
.then((data)=>{
    const stripe = Stripe(data.publicKey)
    
    document.querySelector('#purchasebtn').addEventListener('click',(e)=>{
        e.preventDefault()
        let url = document.querySelector('#url').value
        let amt = parseFloat(document.querySelector(".famt>span").innerHTML)
        let pid = document.querySelector('#purchasebtn').getAttribute('data-productid')
        let name = document.querySelector('#id_name').value
        let city = document.querySelector('#id_city').value
        let address = document.querySelector('#id_address').value
        let state = document.querySelector('#id_state').value
        let country = document.querySelector('#id_country').value
        let phone = document.querySelector('#id_phone').value
        let zipcode = document.querySelector('#id_zipcode').value
        let subject = document.querySelector('#id_subject').value
        let email = document.querySelector('#id_email').value
        let message = document.querySelector('#id_message').value


        console.log("url",url)
        console.log("amount",amt)
        console.log("name",name)
        console.log("city",city)
        console.log("address",address)
        console.log("state",state)
        console.log("country",country)
        console.log("phone",phone)
        console.log("zipcode",zipcode)
        console.log("subject",subject)
        console.log("email",email)
        console.log("message",message)

        fetch('/'+url+'/?price='+amt+"&pid="+pid)
        .then((result)=>{
            $.ajax({
                type: "POST",
                url: "/save_checkout/",
                data: {
                    name:name,
                    city:city,
                    address:address,
                    state:state,
                    country:country,
                    phone:phone,
                    zipcode:zipcode,
                    subject:subject,
                    email:email,
                    message:message,
                },
                success: function (response) {
                    console.log(response)
                }
            });
            return result.json();
        })
        .then((data)=>{
            console.log(data);
            return stripe.redirectToCheckout({sessionId:data.sessionId})
        }).
        then((res)=>{
            console.log(res)
        })
    });
});