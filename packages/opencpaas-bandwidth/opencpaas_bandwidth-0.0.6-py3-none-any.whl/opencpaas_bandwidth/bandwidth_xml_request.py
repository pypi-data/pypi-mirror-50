BANDWIDTH_ORDER_NUMBER =  '<?xml version="1.0" encoding="UTF-8"?>\
                            <Order>\
                            <ExistingTelephoneNumberOrderType>\
                                <TelephoneNumberList>\
                                    <TelephoneNumber>{phone_number}</TelephoneNumber>\
                                </TelephoneNumberList>\
                            </ExistingTelephoneNumberOrderType>\
                            <SiteId>{site_id}</SiteId>\
                        </Order>'

BANDWIDTH_ORDER_NUMBERS = '<?xml version="1.0" encoding="UTF-8"?>\
                            <Order> \
                            <AreaCodeSearchAndOrderType> \
                                <AreaCode>{area_code}</AreaCode> \
                                <Quantity>{quantity}</Quantity> \
                            </AreaCodeSearchAndOrderType> \
                            <SiteId>{site_id}</SiteId>\
                        </Order>'

BANDWIDTH_RELEASE_NUMBER = '<?xml version="1.0" encoding="UTF-8"?>\
                        <DisconnectTelephoneNumberOrder>\
                            <name></name>\
                            <DisconnectTelephoneNumberOrderType>\
                                <TelephoneNumberList>\
                                    <TelephoneNumber>{phone_number}</TelephoneNumber>\
                                </TelephoneNumberList>\
                            </DisconnectTelephoneNumberOrderType>\
                        </DisconnectTelephoneNumberOrder>'