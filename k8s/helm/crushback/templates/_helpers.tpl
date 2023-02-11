{{/*
Expand the name of the chart.
*/}}
{{- define "crushback.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "crushback.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "crushback.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "crushback.labels" -}}
helm.sh/chart: {{ include "crushback.chart" . }}
{{ include "crushback.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Backend labels
*/}}
{{- define "crushback.labels.backend" -}}
{{ include "crushback.labels" }}
{{ include "crushback.selectorLabels.backend" . }}
{{- end }}

{{/*
Frontend labels
*/}}
{{- define "crushback.labels.frontend" -}}
{{ include "crushback.labels" }}
{{ include "crushback.selectorLabels.frontend" . }}
{{- end }}

{{/*
Common selector labels
*/}}
{{- define "crushback.selectorLabels" -}}
app.kubernetes.io/name: {{ include "crushback.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Backend selector labels
*/}}
{{- define "crushback.selectorLabels.backend" -}}
{{ include "crushback.selectorLabels" . }}
crushback/service: backend
{{- end }}

{{/*
Frontend selector labels
*/}}
{{- define "crushback.selectorLabels.frontend" -}}
{{ include "crushback.selectorLabels" . }}
crushback/service: frontend
{{- end }}
