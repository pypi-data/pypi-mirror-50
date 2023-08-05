/**
Copyright (c) 2016-2019 cloudover.io ltd.

Licensee holding a valid commercial license for dinemic library may use it with
accordance to terms of the license agreement between cloudover.io ltd. and the
licensee, or on GNU Affero GPL v3 license terms.

Licensee not holding a valid commercial license for dinemic library may use it
under GNU Affero GPL v3 license.

Terms of GNU Affero GPL v3 license are available on following site:
https://www.gnu.org/licenses/agpl-3.0.en.html
*/

#include "pyaction.h"
#include "module.h"

using namespace std;

PyAction::PyAction(PyObject *self_ptr)
    : self(self_ptr)
{
    if (py_sync == NULL || py_store == NULL) {
        throw Dinemic::DException("Dinemic is not initialized. Call pydinemic.launch first");
    }
}

PyAction::PyAction(PyObject *self_ptr, const PyAction &f)
    : self(self_ptr)
{

}

void PyAction::py_apply(const string &filter) {
    py_sync->add_on_create_listener(filter, this);
    py_sync->add_on_created_listener(filter, this);
    py_sync->add_on_update_listener(filter, this);
    py_sync->add_on_updated_listener(filter, this);
}

void PyAction::py_revoke(const string &filter) {
    py_sync->remove_on_create_listener(filter, this);
    py_sync->remove_on_created_listener(filter, this);
    py_sync->remove_on_update_listener(filter, this);
    py_sync->remove_on_updated_listener(filter, this);
}

void PyAction::call_listener(const string &name, PyObject *args) {
    if (PyObject_HasAttrString(self, name.c_str())) {
        PyObject *method = PyObject_GetAttrString(self, name.c_str());
        PyObject *keywords = PyDict_New();
        if (keywords == NULL) {
            return;
        }
        if (args == NULL) {
            return;
        }
        if (method == NULL) {
            return;
        }
        PyObject *result = PyObject_Call(method, args, keywords);
        PyObject *err = PyErr_Occurred();
        Py_DECREF(keywords);
        Py_XDECREF(method);
        Py_XDECREF(result);
        if (err) {
            throw Dinemic::DUpdateRejected(string("Python threw an exception: ") + err->ob_type->tp_name);
            // After docs:
            // You do not own a reference to the return value, so you do not need to Py_DECREF() it.
        }
    }
}

void PyAction::on_create(Dinemic::DActionContext &context, const std::string &key) {
    PyObject *args = Py_BuildValue("ss", context.get_object_id().c_str(), key.c_str());
    call_listener("on_create", args);
    Py_DECREF(args);

    Dinemic::DAction::on_create(context, key);
}

void PyAction::on_created(Dinemic::DActionContext &context, const std::string &key) {
    PyObject *args = Py_BuildValue("ss", context.get_object_id().c_str(), key.c_str());
    call_listener("on_created", args);
    Py_DECREF(args);

    Dinemic::DAction::on_created(context, key);
}

void PyAction::on_owned_created(Dinemic::DActionContext &context, const std::string &key) {
    PyObject *args = Py_BuildValue("ss", context.get_object_id().c_str(), key.c_str());
    call_listener("on_owned_created", args);
    Py_DECREF(args);
}

void PyAction::on_update(Dinemic::DActionContext &context, const string &key, const string &old_value, const string &new_value) {
    PyObject *args = Py_BuildValue("(ss#s#s#)", context.get_object_id().c_str(), key.c_str(), key.size(), old_value.c_str(), old_value.size(), new_value.c_str(), new_value.size());
    call_listener("on_update", args);
    Py_DECREF(args);

    Dinemic::DAction::on_update(context, key, old_value, new_value);
}

void PyAction::on_authorized_update(Dinemic::DActionContext &context, const string &key, const string &old_value, const string &new_value) {
    PyObject *args = Py_BuildValue("(ss#s#s#)", context.get_object_id().c_str(), key.c_str(), key.size(), old_value.c_str(), old_value.size(), new_value.c_str(), new_value.size());
    call_listener("on_authorized_update", args);
    Py_DECREF(args);
}

void PyAction::on_unauthorized_update(Dinemic::DActionContext &context, const string &key, const string &old_value, const string &new_value) {
    PyObject *args = Py_BuildValue("(ss#s#s#)", context.get_object_id().c_str(), key.c_str(), key.size(), old_value.c_str(), old_value.size(), new_value.c_str(), new_value.size());
    call_listener("on_unauthorized_update", args);
    Py_DECREF(args);
}

void PyAction::on_owned_update(Dinemic::DActionContext &context, const string &key, const string &old_value, const string &new_value) {
    PyObject *args = Py_BuildValue("(ss#s#s#)", context.get_object_id().c_str(), key.c_str(), key.size(), old_value.c_str(), old_value.size(), new_value.c_str(), new_value.size());
    call_listener("on_owned_update", args);
    Py_DECREF(args);
}

void PyAction::on_updated(Dinemic::DActionContext &context, const string &key, const string &old_value, const string &new_value) {
    PyObject *args = Py_BuildValue("(ss#s#s#)", context.get_object_id().c_str(), key.c_str(), key.size(), old_value.c_str(), old_value.size(), new_value.c_str(), new_value.size());
    call_listener("on_updated", args);
    Py_DECREF(args);

    Dinemic::DAction::on_updated(context, key, old_value, new_value);
}

void PyAction::on_authorized_updated(Dinemic::DActionContext &context, const string &key, const string &old_value, const string &new_value) {
    PyObject *args = Py_BuildValue("(ss#s#s#)", context.get_object_id().c_str(), key.c_str(), key.size(), old_value.c_str(), old_value.size(), new_value.c_str(), new_value.size());
    call_listener("on_authorized_updated", args);
    Py_DECREF(args);
}

void PyAction::on_unauthorized_updated(Dinemic::DActionContext &context, const string &key, const string &old_value, const string &new_value) {
    PyObject *args = Py_BuildValue("(ss#s#s#)", context.get_object_id().c_str(), key.c_str(), key.size(), old_value.c_str(), old_value.size(), new_value.c_str(), new_value.size());
    call_listener("on_unauthorized_updated", args);
    Py_DECREF(args);
}

void PyAction::on_owned_updated(Dinemic::DActionContext &context, const string &key, const string &old_value, const string &new_value) {
    PyObject *args = Py_BuildValue("(ss#s#s#)", context.get_object_id().c_str(), key.c_str(), key.size(), old_value.c_str(), old_value.size(), new_value.c_str(), new_value.size());
    call_listener("on_owned_updated", args);
    Py_DECREF(args);
}

void PyAction::on_delete(Dinemic::DActionContext &context, const string &key, const string &value) {
    PyObject *args = Py_BuildValue("(ss#s#)", context.get_object_id().c_str(), key.c_str(), key.size(), value.c_str(), value.size());
    call_listener("on_delete", args);
    Py_DECREF(args);

    Dinemic::DAction::on_delete(context, key, value);
}

void PyAction::on_authorized_delete(Dinemic::DActionContext &context, const string &key, const string &value) {
    PyObject *args = Py_BuildValue("(ss#s#)", context.get_object_id().c_str(), key.c_str(), key.size(), value.c_str(), value.size());
    call_listener("on_authorized_delete", args);
    Py_DECREF(args);
}

void PyAction::on_unauthorized_delete(Dinemic::DActionContext &context, const string &key, const string &value) {
    PyObject *args = Py_BuildValue("(ss#s#)", context.get_object_id().c_str(), key.c_str(), key.size(), value.c_str(), value.size());
    call_listener("on_unauthorized_delete", args);
    Py_DECREF(args);
}

void PyAction::on_owned_delete(Dinemic::DActionContext &context, const string &key, const string &value) {
    PyObject *args = Py_BuildValue("(ss#s#)", context.get_object_id().c_str(), key.c_str(), key.size(), value.c_str(), value.size());
    call_listener("on_owned_delete", args);
    Py_DECREF(args);
}

void PyAction::on_deleted(Dinemic::DActionContext &context, const string &key, const string &value) {
    PyObject *args = Py_BuildValue("(ss#s#)", context.get_object_id().c_str(), key.c_str(), key.size(), value.c_str(), value.size());
    call_listener("on_deleted", args);
    Py_DECREF(args);

    Dinemic::DAction::on_deleted(context, key, value);
}

void PyAction::on_authorized_deleted(Dinemic::DActionContext &context, const string &key, const string &value) {
    PyObject *args = Py_BuildValue("(ss#s#)", context.get_object_id().c_str(), key.c_str(), key.size(), value.c_str(), value.size());
    call_listener("on_authorized_deleted", args);
    Py_DECREF(args);
}

void PyAction::on_unauthorized_deleted(Dinemic::DActionContext &context, const string &key, const string &value) {
    PyObject *args = Py_BuildValue("(ss#s#)", context.get_object_id().c_str(), key.c_str(), key.size(), value.c_str(), value.size());
    call_listener("on_unauthorized_deleted", args);
    Py_DECREF(args);
}

void PyAction::on_owned_deleted(Dinemic::DActionContext &context, const string &key, const string &value) {
    PyObject *args = Py_BuildValue("(ss#s#)", context.get_object_id().c_str(), key.c_str(), key.size(), value.c_str(), value.size());
    call_listener("on_owned_deleted", args);
    Py_DECREF(args);
}

void PyAction::on_remove(Dinemic::DActionContext &context) {
    PyObject *args = Py_BuildValue("s", context.get_object_id().c_str());
    call_listener("on_remove", args);
    Py_DECREF(args);

    Dinemic::DAction::on_remove(context);
}

void PyAction::on_authorized_remove(Dinemic::DActionContext &context) {
    PyObject *args = Py_BuildValue("s", context.get_object_id().c_str());
    call_listener("on_authorized_remove", args);
    Py_DECREF(args);
}

void PyAction::on_unauthorized_remove(Dinemic::DActionContext &context) {
    PyObject *args = Py_BuildValue("s", context.get_object_id().c_str());
    call_listener("on_unauthorized_remove", args);
    Py_DECREF(args);
}

void PyAction::on_owned_remove(Dinemic::DActionContext &context) {
    PyObject *args = Py_BuildValue("s", context.get_object_id().c_str());
    call_listener("on_owned_remove", args);
    Py_DECREF(args);
}
