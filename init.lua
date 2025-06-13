local lspconfig = require("lspconfig")

lspconfig.ruff.setup(
    {
        on_attach = function(client, bufnr)
            if client.supports_method("textDocument/formatting") then
                vim.api.nvim_create_autocmd(
                    "BufWritePre",
                    {
                        group = vim.api.nvim_create_augroup("LspFormattingRuff", {clear = true}),
                        buffer = bufnr,
                        callback = function()
                            vim.lsp.buf.format({bufnr = bufnr})
                            vim.lsp.buf.code_action(
                                {
                                    bufnr = bufnr,
                                    context = {
                                        only = {"source.organizeImports"}
                                    },
                                    apply = true
                                }
                            )
                        end
                    }
                )
            end
        end
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
