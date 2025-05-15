local lspconfig = require("lspconfig")

lspconfig.ruff.setup(
    {
        on_attach = function(client, bufnr)
            vim.api.nvim_create_autocmd(
                "BufWritePre",
                {
                    buffer = bufnr,
                    callback = function()
                        vim.lsp.buf.format({bufnr = bufnr})
                    end
                }
            )
        end,
        init_options = {
            settings = {
                ruff = {
                    formatOnSave = true
                }
            }
        }
    }
)

lspconfig.pyright.setup(
    {
        capabilities = (function()
            local capabilities = vim.lsp.protocol.make_client_capabilities()
            capabilities.textDocument.publishDiagnostics.tagSupport.valueSet = {2}
            return capabilities
        end)(),
        settings = {
            pyright = {
                -- Using Ruff's import organizer
                disableOrganizeImports = true
            },
            python = {
                typeCheckingMode = "strict",
                analysis = {
                    useLibraryCodeForTypes = true,
                    autoSearchPaths = true,
                    diagnosticMode = "openFilesOnly",
                    diagnosticSeverityOverrides = {
                        reportUnusedVariable = "warning"
                    }
                }
            }
        }
    }
)
