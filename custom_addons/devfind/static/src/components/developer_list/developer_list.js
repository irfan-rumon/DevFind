// File: static/src/components/developer_list/developer_list.js
/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

class DeveloperListComponent extends Component {
    setup() {
        this.orm = useService("orm");
        this.state = {
            developers: [],
            loading: true,
        };
        this.loadDevelopers();
    }

    async loadDevelopers() {
        try {
            const developers = await this.orm.searchRead(
                'devfind.developer',
                [],
                ['name', 'email', 'technologies_list', 'min_hourly_rate', 'max_hourly_rate']
            );
            this.state.developers = developers;
        } catch (error) {
            console.error('Error loading developers:', error);
        } finally {
            this.state.loading = false;
        }
    }
}

DeveloperListComponent.template = 'devfind.DeveloperList';

registry.category("actions").add("devfind.developer_list_action", DeveloperListComponent);