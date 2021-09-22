const searchField = document.getElementById('searchField')
const tableContainer = document.getElementById('table-container')
const tableSearchContainer = document.getElementById('table-search-container')
const paginationContainer = document.getElementById('pagination-container')
const tableSearchBody = document.getElementById('table-search-body')
const noResults = document.getElementById('no-results')

const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value

tableSearchContainer.style.display = 'none'

searchField.addEventListener('keyup', (e) => {
    const searchText = e.target.value

    if(searchText.trim().length > 0) {
        $.ajax({
            type: "post",
            url: "/search-expenses/",
            data: {
              "searchText": searchText,
              "csrfmiddlewaretoken": csrf,
            },
            success: (res) => {
              tableSearchBody.innerHTML = ''

              tableContainer.style.display = 'none'
              tableSearchContainer.style.display = 'block'

              if(res.length === 0) {
                paginationContainer.style.display = 'none'
                tableSearchContainer.style.display = 'none'
                noResults.style.display = 'block'
              } else {
                noResults.style.display = 'none'
                res.forEach(item => {
                    tableSearchBody.innerHTML += `
                        <tr>
                            <td>${item.amount}</td>
                            <td>${item.category}</td>
                            <td>${item.description}</td>
                            <td>${item.date}</td>
                        </tr>
                    `
                })
              }
            },
            error: (jqXHR, errorThrown, textStatus) => {
                console.log(errorThrown)
            },
        });
    } else {
        tableContainer.style.display = 'block'
        paginationContainer.style.display = 'block'
        tableSearchContainer.style.display = 'none'
    }
})