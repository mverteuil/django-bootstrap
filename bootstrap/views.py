from django.core.urlresolvers import reverse

from django.contrib import messages

from django.views.generic import (ListView as BaseListView,
                                  DetailView as BaseDetailView)

from django.views.generic.edit import (FormView as BaseFormView,
                                       CreateView as BaseCreateView,
                                       UpdateView as BaseUpdateView,
                                       DeleteView as BaseDeleteView)


class ListView(BaseListView):
    def get_template_names(self):
        templates = super(ListView, self).get_template_names()
        templates.append('bootstrap/list.html')
        return templates

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)

        model_meta = self.model._meta

        context['section'] = model_meta.verbose_name.lower()
        context['model_verbose_name'] = model_meta.verbose_name
        context['model_verbose_name_plural'] = model_meta.verbose_name_plural

        context['add_object_url'] = self._get_create_url()

        return context

    def _get_create_url(self):
        model_meta = self.model._meta
        app_label = model_meta.app_label
        name = model_meta.object_name.lower()

        return reverse('%s:%s_form' % (app_label, name))


class DetailView(BaseDetailView):
    def get_template_names(self):
        templates = super(DetailView, self).get_template_names()
        templates.append('bootstrap/detail.html')
        return templates

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        model_meta = self.model._meta
        context['section'] = model_meta.verbose_name.lower()
        context['name'] = self._get_name()
        context['edit_object_url'] = self._get_edit_url()
        context['delete_object_url'] = self._get_delete_url()
        context['model_verbose_name'] = model_meta.verbose_name
        context['model_verbose_name_plural'] = model_meta.verbose_name_plural

        return context

    def _get_name(self):
        obj = self.get_object()
        if hasattr(obj, "name"):
            return obj.name
        else:
            return None

    def _get_edit_url(self):
        model_meta = self.model._meta
        app_label = model_meta.app_label
        name = model_meta.object_name.lower()
        pk = self.kwargs.get('pk', None)
        return reverse('%s:%s_form' % (app_label, name), args=(pk,))

    def _get_delete_url(self):
        model_meta = self.model._meta
        app_label = model_meta.app_label
        name = model_meta.object_name.lower()
        pk = self.kwargs.get('pk', None)
        return reverse('%s:%s_delete' % (app_label, name), args=(pk,))


class FormView(BaseFormView):
    def get_context_data(self, **kwargs):
        context = super(FormView, self).get_context_data(**kwargs)

        form_meta = self.get_form_class()._meta
        model_meta = form_meta.model._meta

        context['section'] = model_meta.verbose_name.lower()
        context['model_verbose_name'] = model_meta.verbose_name
        context['model_verbose_name_plural'] = model_meta.verbose_name_plural

        context['success_url'] = self.get_success_url()

        return context

    def get_success_url(self):
        form_meta = self.get_form_class()._meta
        model_meta = form_meta.model._meta

        app_label = model_meta.app_label
        name = model_meta.object_name.lower()

        return reverse('%s:%s_list' % (app_label, name))

    def _get_model_verbose_name(self):
        model_meta = self.form_class._meta.model._meta

        return (model_meta.verbose_name,
                model_meta.verbose_name_plural)


class CreateView(FormView, BaseCreateView):
    def get_template_names(self):
        templates = super(CreateView, self).get_template_names()
        templates.append('bootstrap/create.html')
        return templates

    def form_valid(self, form):
        verbose_name = self._get_model_verbose_name()[0]
        messages.success(self.request, '%s "%s" added' % (verbose_name, form.instance))
        return super(CreateView, self).form_valid(form)


class UpdateView(FormView, BaseUpdateView):
    def get_template_names(self):
        templates = super(UpdateView, self).get_template_names()
        templates.append('bootstrap/update.html')
        return templates

    def form_valid(self, form):
        verbose_name = self._get_model_verbose_name()[0]
        messages.success(self.request, '%s "%s" updated' % (verbose_name, form.instance))
        return super(UpdateView, self).form_valid(form)

    def get_queryset(self):
        form = self.get_form_class()
        model = form._meta.model
        return model.objects.filter(pk=self.kwargs.get('pk', None))

    def get_object(self):
        return self.get_queryset().get()

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        context['delete_url'] = self._get_delete_url()
        return context

    def _get_delete_url(self):
        form_meta = self.get_form_class()._meta
        model_meta = form_meta.model._meta
        app_label = model_meta.app_label
        name = model_meta.object_name.lower()
        pk = self.kwargs.get('pk', None)
        return reverse('%s:%s_delete' % (app_label, name), args=(pk,))


class DeleteView(BaseDeleteView):
    def get_template_names(self):
        templates = super(DeleteView, self).get_template_names()
        templates.append('bootstrap/delete.html')
        return templates

    def delete(self, *args, **kwargs):
        instance = self.get_object()
        verbose_name = self._get_model_verbose_name()[0]
        messages.success(self.request, '%s "%s" deleted' % (verbose_name, instance))
        return super(DeleteView, self).delete(*args, **kwargs)

    def _get_model_verbose_name(self):
        model_meta = self.model._meta

        return (model_meta.verbose_name,
                model_meta.verbose_name_plural)

    def get_context_data(self, **kwargs):
        context = super(DeleteView, self).get_context_data(**kwargs)

        model_meta = self.model._meta

        context['section'] = model_meta.verbose_name.lower()
        context['model_verbose_name'] = model_meta.verbose_name
        context['model_verbose_name_plural'] = model_meta.verbose_name_plural

        context['success_url'] = self.get_success_url()

        return context

    def get_success_url(self):
        model_meta = self.model._meta

        app_label = model_meta.app_label
        name = model_meta.object_name.lower()

        return reverse('%s:%s_list' % (app_label, name))
