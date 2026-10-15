import json

from llm.schemas import CRMContractResponse
from main import main


def test_main(monkeypatch, capsys):
    response = CRMContractResponse(
        contract_id="C-100",
        contract_terms=["Renewal term: 12 months"],
        active_addons=["Premium Support"],
        found_in_context=True,
    )

    monkeypatch.setattr("main.ask_crm_question", lambda **kwargs: response)

    main()

    captured = capsys.readouterr()
    lines = captured.out.splitlines()

    assert lines[0] == "CRM Agent - Contract and Add-on Retrieval"
    assert json.loads("\n".join(lines[1:])) == response.model_dump()
