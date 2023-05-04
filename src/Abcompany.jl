
module Abcompany
using Dash

const resources_path = realpath(joinpath( @__DIR__, "..", "deps"))
const version = "1.0.0"

include("jl/logincomponent.jl")
include("jl/examplecomponent.jl")

function __init__()
    DashBase.register_package(
        DashBase.ResourcePkg(
            "abcompany",
            resources_path,
            version = version,
            [
                DashBase.Resource(
    relative_package_path = "abcompany.js",
    external_url = "https://unpkg.com/abcompany@1.0.0/abcompany/abcompany.js",
    dynamic = nothing,
    async = nothing,
    type = :js
),
DashBase.Resource(
    relative_package_path = "abcompany.js.map",
    external_url = "https://unpkg.com/abcompany@1.0.0/abcompany/abcompany.js.map",
    dynamic = true,
    async = nothing,
    type = :js
)
            ]
        )

    )
end
end
