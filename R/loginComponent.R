# AUTO GENERATED FILE - DO NOT EDIT

#' @export
loginComponent <- function(id=NULL) {
    
    props <- list(id=id)
    if (length(props) > 0) {
        props <- props[!vapply(props, is.null, logical(1))]
    }
    component <- list(
        props = props,
        type = 'LoginComponent',
        namespace = 'abcompany',
        propNames = c('id'),
        package = 'abcompany'
        )

    structure(component, class = c('dash_component', 'list'))
}
