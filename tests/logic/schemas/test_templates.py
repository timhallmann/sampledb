import sampledb.logic


def test_update_template_action():
    template_action = sampledb.logic.actions.create_action(
        action_type_id=sampledb.logic.actions.ActionType.TEMPLATE,
        schema={
            'title': 'Test Template',
            'type': 'object',
            'properties': {
                'name': {
                    'title': 'Name',
                    'type': 'text'
                },
                'value': {
                    'title': 'Value',
                    'type': 'text'
                }
            },
            'required': ['name']
        }
    )
    including_action = sampledb.logic.actions.create_action(
        action_type_id=sampledb.logic.actions.ActionType.SAMPLE_CREATION,
        schema={
            'title': 'Test Action',
            'type': 'object',
            'properties': {
                'name': {
                    'title': 'Name',
                    'type': 'text'
                },
                'template': {
                    'title': 'Template',
                    'type': 'object',
                    'template': template_action.id
                }
            },
            'required': ['name']
        }
    )
    assert including_action.schema == {
        'title': 'Test Action',
        'type': 'object',
        'properties': {
            'name': {
                'title': 'Name',
                'type': 'text'
            },
            'template': {
                'title': 'Template',
                'type': 'object',
                'template': template_action.id,
                'properties': {
                    'value': {
                        'title': 'Value',
                        'type': 'text'
                    }
                },
                'required': []
            }
        },
        'required': ['name']
    }
    sampledb.logic.actions.update_action(
        action_id=template_action.id,
        schema={
            'title': 'Test Template',
            'type': 'object',
            'properties': {
                'name': {
                    'title': 'Name',
                    'type': 'text'
                },
                'value': {
                    'title': 'Value',
                    'type': 'object_reference'
                }
            },
            'required': ['name', 'value']
        }
    )
    including_action = sampledb.logic.actions.get_action(including_action.id)
    assert including_action.schema == {
        'title': 'Test Action',
        'type': 'object',
        'properties': {
            'name': {
                'title': 'Name',
                'type': 'text'
            },
            'template': {
                'title': 'Template',
                'type': 'object',
                'template': template_action.id,
                'properties': {
                    'value': {
                        'title': 'Value',
                        'type': 'object_reference'
                    }
                },
                'required': ['value']
            }
        },
        'required': ['name']
    }


def test_update_template_action_recursion():
    template_action = sampledb.logic.actions.create_action(
        action_type_id=sampledb.logic.actions.ActionType.TEMPLATE,
        schema={
            'title': 'Test Template',
            'type': 'object',
            'properties': {
                'name': {
                    'title': 'Name',
                    'type': 'text'
                },
                'value': {
                    'title': 'Value',
                    'type': 'text'
                }
            },
            'required': ['name']
        }
    )
    including_template_action = sampledb.logic.actions.create_action(
        action_type_id=sampledb.logic.actions.ActionType.TEMPLATE,
        schema={
            'title': 'Including Template Action',
            'type': 'object',
            'properties': {
                'name': {
                    'title': 'Name',
                    'type': 'text'
                },
                'template1': {
                    'title': 'Template',
                    'type': 'object',
                    'template': template_action.id
                }
            },
            'required': ['name']
        }
    )
    assert including_template_action.schema == {
        'title': 'Including Template Action',
        'type': 'object',
        'properties': {
            'name': {
                'title': 'Name',
                'type': 'text'
            },
            'template1': {
                'title': 'Template',
                'type': 'object',
                'template': template_action.id,
                'properties': {
                    'value': {
                        'title': 'Value',
                        'type': 'text'
                    }
                },
                'required': []
            }
        },
        'required': ['name']
    }
    including_action = sampledb.logic.actions.create_action(
        action_type_id=sampledb.logic.actions.ActionType.TEMPLATE,
        schema={
            'title': 'Including Action',
            'type': 'object',
            'properties': {
                'name': {
                    'title': 'Name',
                    'type': 'text'
                },
                'template': {
                    'title': 'Template',
                    'type': 'object',
                    'template': including_template_action.id
                }
            },
            'required': ['name']
        }
    )
    assert including_action.schema == {
        'title': 'Including Action',
        'type': 'object',
        'properties': {
            'name': {
                'title': 'Name',
                'type': 'text'
            },
            'template': {
                'title': 'Template',
                'type': 'object',
                'template': including_template_action.id,
                'properties': {
                    'template1': {
                        'title': 'Template',
                        'type': 'object',
                        'template': template_action.id,
                        'properties': {
                            'value': {
                                'title': 'Value',
                                'type': 'text'
                            }
                        },
                        'required': []
                    }
                },
                'required': []
            }
        },
        'required': ['name']
    }

    # updating template_action should trigger an update in including_template_action and including_action
    sampledb.logic.actions.update_action(
        action_id=template_action.id,
        schema={
            'title': 'Test Template',
            'type': 'object',
            'properties': {
                'name': {
                    'title': 'Name',
                    'type': 'text'
                },
                'value': {
                    'title': 'Value',
                    'type': 'object_reference'
                }
            },
            'required': ['name', 'value']
        }
    )
    including_action = sampledb.logic.actions.get_action(including_action.id)
    assert including_action.schema == {
        'title': 'Including Action',
        'type': 'object',
        'properties': {
            'name': {
                'title': 'Name',
                'type': 'text'
            },
            'template': {
                'title': 'Template',
                'type': 'object',
                'template': including_template_action.id,
                'properties': {
                    'template1': {
                        'title': 'Template',
                        'type': 'object',
                        'template': template_action.id,
                        'properties': {
                            'value': {
                                'title': 'Value',
                                'type': 'object_reference'
                            }
                        },
                        'required': ['value']
                    }
                },
                'required': []
            }
        },
        'required': ['name']
    }
    including_template_action = sampledb.logic.actions.get_action(including_template_action.id)
    assert including_template_action.schema == {
        'title': 'Including Template Action',
        'type': 'object',
        'properties': {
            'name': {
                'title': 'Name',
                'type': 'text'
            },
            'template1': {
                'title': 'Template',
                'type': 'object',
                'template': template_action.id,
                'properties': {
                    'value': {
                        'title': 'Value',
                        'type': 'object_reference'
                    }
                },
                'required': ['value']
            }
        },
        'required': ['name']
    }

    # updating including_template_action should trigger an update in including_action
    sampledb.logic.actions.update_action(
        action_id=including_template_action.id,
        schema={
            'title': 'Including Template Action',
            'type': 'object',
            'properties': {
                'name': {
                    'title': 'Name',
                    'type': 'text'
                },
                'template1': {
                    'title': 'Template',
                    'type': 'object',
                    'template': template_action.id,
                    'properties': {},
                    'required': []
                },
                'template2': {
                    'title': 'Template',
                    'type': 'object',
                    'template': template_action.id,
                    'properties': {},
                    'required': []
                }
            },
            'required': ['name']
        }
    )
    including_action = sampledb.logic.actions.get_action(including_action.id)
    assert including_action.schema == {
        'title': 'Including Action',
        'type': 'object',
        'properties': {
            'name': {
                'title': 'Name',
                'type': 'text'
            },
            'template': {
                'title': 'Template',
                'type': 'object',
                'template': including_template_action.id,
                'properties': {
                    'template1': {
                        'title': 'Template',
                        'type': 'object',
                        'template': template_action.id,
                        'properties': {
                            'value': {
                                'title': 'Value',
                                'type': 'object_reference'
                            }
                        },
                        'required': ['value']
                    },
                    'template2': {
                        'title': 'Template',
                        'type': 'object',
                        'template': template_action.id,
                        'properties': {
                            'value': {
                                'title': 'Value',
                                'type': 'object_reference'
                            }
                        },
                        'required': ['value']
                    }
                },
                'required': []
            }
        },
        'required': ['name']
    }
    including_template_action = sampledb.logic.actions.get_action(including_template_action.id)
    assert including_template_action.schema == {
        'title': 'Including Template Action',
        'type': 'object',
        'properties': {
            'name': {
                'title': 'Name',
                'type': 'text'
            },
            'template1': {
                'title': 'Template',
                'type': 'object',
                'template': template_action.id,
                'properties': {
                    'value': {
                        'title': 'Value',
                        'type': 'object_reference'
                    }
                },
                'required': ['value']
            },
            'template2': {
                'title': 'Template',
                'type': 'object',
                'template': template_action.id,
                'properties': {
                    'value': {
                        'title': 'Value',
                        'type': 'object_reference'
                    }
                },
                'required': ['value']
            }
        },
        'required': ['name']
    }