const contentContainer = document.getElementById('content-container')
const loginForm = document.getElementById('login-form')
const searchForm = document.getElementById('search-form')
const baseEndpoint = "http://localhost:8000/api"
if (loginForm) {
  loginForm.addEventListener('submit', handleLogin)
}
if (searchForm) {
  searchForm.addEventListener('submit', handleSearch)
}

function handleLogin(event) {
  console.log(event)
  event.preventDefault()
  const loginEndpoint = `${baseEndpoint}/token/`
  let loginFormData = new FormData(loginForm)
  let loginObjectData = Object.fromEntries(loginFormData)
  console.log(loginObjectData)
  const options = {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(loginObjectData)
  }
  fetch(loginEndpoint, options).then(response => {
    return response.json()
  }).then(authData => {
    handleAuthData(authData, getProductList)
  })
  .catch(err => {
    console.log('error: ', err)
  })
}

function handleSearch(event) {
  event.preventDefault()

  let formData = new FormData(searchForm)
  let data = Object.fromEntries(formData)
  let searchParams = new URLSearchParams(data)
  const endpoint = `${baseEndpoint}/search?${searchParams}`
  const headers = {
    "Content-Type": "application/json",
  }
  const authToken = localStorage.getItem('access')
  if (authToken) {
    headers['Authorization'] = `Bearer ${authToken}`
  }
  const options = {
    method: "GET",
    headers:headers
  }
  fetch(endpoint, options).then(response => {
    return response.json()
  }).then(data => {
    const validData = isTokenNotValid(data)
    if (validData && contentContainer) {
      contentContainer.innerHTML = ""
      if (data && data.hits) {
        let htmlStr = ""
        for (let result of data.hits) {
          htmlStr += "<li>" + result.title + "</li>"
        }
        contentContainer.innerHTML = htmlStr
        if (data.hits.length === 0) {
          contentContainer.innerHTML = "<p>No results found</p>"
        }
      } else {
        contentContainer.innerHTML = "<p>No results found</p>"
      }
    }
  })
  .catch(err => {
    console.log('error: ', err)
  })
}

function handleAuthData(authData, callback) {
  localStorage.setItem('access', authData.access)
  localStorage.setItem('refresh', authData.refresh)
  if (callback) {
    callback()
  }
}

function writeToContainer(data) {
  if (contentContainer) {
    contentContainer.innerHTML = "<pre>" + JSON.stringify(data) + "</pre>"
  }
}
function getFetchOptions(method, body) {
  return {
    method: method == null ? "GET" : method,
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${localStorage.getItem('access')}`
    },
    body: body ? body : null
  }
}

function isTokenNotValid(jsonData) {
  if (jsonData.code && jsonData == "token_not_valid") {
    alert("Please login again")
    return false
  }
  return true
}

function getProductList() {
  const endpoint = `${baseEndpoint}/products/`
  const options = getFetchOptions()
  fetch(endpoint, options).then(response => response.json()).then(data => {
    const validData = isTokenNotValid(data)
    if (validData) {
      writeToContainer(data)
    }
  })
}

const searchClient = algoliasearch('O0X2FMM7J3', 'cb5515df7f7c99eda67f0217534ff11d');

const search = instantsearch({
  indexName: 'godfreyowidi_Product',
  searchClient,
});

search.addWidgets([
  instantsearch.widgets.searchBox({
    container: '#searchBox',
  }),

instantsearch.widgets.clearRefinements({
  container: "#clear-refinements"
}),

instantsearch.widgets.refinementList({
  container: "#user-list",
  attribute: "user"
}),

  instantsearch.widgets.hits({
    container: '#hits',
    templates: {
      item: `<div>{{ title }}<p>{{ user }}</p><p>\${{ price }}</div>`
    }
  })
]);

search.start();
