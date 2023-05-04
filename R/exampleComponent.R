# AUTO GENERATED FILE - DO NOT EDIT

#' @export
exampleComponent <- function(id=NULL) {
    
    props <- list(id=id)
    if (length(props) > 0) {
        props <- props[!vapply(props, is.null, logical(1))]
    }
    component <- list(
        props = props,
        type = 'ExampleComponent',
        namespace = 'abcompany',
        propNames = c('id'),
        package = 'abcompany'
        )

    structure(component, class = c('dash_component', 'list'))
}
