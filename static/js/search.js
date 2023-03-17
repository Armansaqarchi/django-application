let search_form = document.getElementById("saerch_form")
let page_links = document.getElementsByClassName("page-link")

if(search_form){
for (let i = 0; i < page_links.length; i++){
    page_links[i].addEventListener("click", function(e) {
        //in order to make search bar agrorithm remain, need to disable default and add search bar anytime clicking on the new page
        e.preventDefault()
        
        //need to take the current page and add the new search parameter
        let page = this.dataset.page

        //adding new input to the page inside the html form
        search_form.innerHTML += `<input value=${page} name=page hidden/>`

        searchForm.submit()
    })
}

}
